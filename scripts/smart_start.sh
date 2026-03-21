#!/usr/bin/env bash
# TradingAgents-CN 一键启动脚本（macOS/Linux）
# 优先使用 Docker Hub 镜像快速启动，失败时自动回退到本地构建。

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
BASE_COMPOSE_FILE="$PROJECT_ROOT/docker-compose.hub.nginx.yml"
ENV_EXAMPLE_FILE="$PROJECT_ROOT/.env.example"
ENV_FILE="$PROJECT_ROOT/.env"

APP_PORT="${APP_PORT:-80}"
PORT_FROM_CLI=false
FORCE_BUILD=false

TEMP_FILES=()

log() {
    printf '[INFO] %s\n' "$1"
}

warn() {
    printf '[WARN] %s\n' "$1"
}

error() {
    printf '[ERROR] %s\n' "$1" >&2
}

usage() {
    cat <<'EOF'
TradingAgents-CN 一键启动脚本

用法:
  ./scripts/smart_start.sh
  ./scripts/smart_start.sh --build
  ./scripts/smart_start.sh --port 8080

参数:
  --build        强制跳过 Docker Hub 镜像，直接本地构建启动
  --port <port>  指定外部访问端口，默认 80
  --help         显示帮助

环境变量:
  APP_PORT       等同于 --port

说明:
  1. 默认优先拉取预构建镜像，适合新设备快速启动
  2. 如果镜像不可用，会自动回退到本地构建
  3. 首次运行会自动从 .env.example 创建 .env
EOF
}

cleanup() {
    local file
    for file in "${TEMP_FILES[@]:-}"; do
        if [[ -n "$file" && -f "$file" ]]; then
            rm -f "$file"
        fi
    done
}

trap cleanup EXIT

while [[ $# -gt 0 ]]; do
    case "$1" in
        --build)
            FORCE_BUILD=true
            shift
            ;;
        --port)
            if [[ $# -lt 2 ]]; then
                error "--port 需要一个端口号"
                exit 1
            fi
            APP_PORT="$2"
            PORT_FROM_CLI=true
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            error "未知参数: $1"
            usage
            exit 1
            ;;
    esac
done

if ! [[ "$APP_PORT" =~ ^[0-9]+$ ]] || (( APP_PORT < 1 || APP_PORT > 65535 )); then
    error "端口无效: $APP_PORT"
    exit 1
fi

resolve_compose_cmd() {
    if docker compose version >/dev/null 2>&1; then
        COMPOSE_CMD=(docker compose)
    elif command -v docker-compose >/dev/null 2>&1; then
        COMPOSE_CMD=(docker-compose)
    else
        error "未检测到 docker compose 或 docker-compose"
        exit 1
    fi
}

compose() {
    "${COMPOSE_CMD[@]}" "$@"
}

require_prerequisites() {
    if ! command -v docker >/dev/null 2>&1; then
        error "未安装 Docker，请先安装 Docker Desktop 或 Docker Engine"
        exit 1
    fi

    if ! command -v curl >/dev/null 2>&1; then
        error "未安装 curl，脚本需要它做健康检查"
        exit 1
    fi

    if ! docker info >/dev/null 2>&1; then
        error "Docker 未运行，请先启动 Docker"
        exit 1
    fi

    if [[ ! -f "$BASE_COMPOSE_FILE" ]]; then
        error "缺少文件: $BASE_COMPOSE_FILE"
        exit 1
    fi

    if [[ ! -f "$ENV_EXAMPLE_FILE" ]]; then
        error "缺少文件: $ENV_EXAMPLE_FILE"
        exit 1
    fi
}

ensure_runtime_dirs() {
    mkdir -p "$PROJECT_ROOT/logs" "$PROJECT_ROOT/data" "$PROJECT_ROOT/nginx"
}

ensure_env_file() {
    if [[ -f "$ENV_FILE" ]]; then
        return
    fi

    cp "$ENV_EXAMPLE_FILE" "$ENV_FILE"
    warn "未找到 .env，已根据 .env.example 自动创建"
    warn "首次分析前请编辑 .env，至少配置一个大模型 API Key"
}

detect_arch() {
    local machine_arch
    machine_arch="$(uname -m)"

    case "$machine_arch" in
        x86_64|amd64)
            ARCH_SUFFIX="amd64"
            ;;
        arm64|aarch64)
            ARCH_SUFFIX="arm64"
            ;;
        *)
            ARCH_SUFFIX="unknown"
            warn "未识别的 CPU 架构: $machine_arch，将直接使用本地构建"
            FORCE_BUILD=true
            ;;
    esac
}

port_in_use() {
    local port="$1"
    lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1
}

find_available_port() {
    local candidate
    for candidate in "$@"; do
        if ! port_in_use "$candidate"; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    return 1
}

ensure_port() {
    if ! port_in_use "$APP_PORT"; then
        return
    fi

    if [[ "$PORT_FROM_CLI" == true ]]; then
        error "端口 $APP_PORT 已被占用，请换一个端口后重试"
        exit 1
    fi

    warn "默认端口 $APP_PORT 已被占用，正在自动选择其它端口"
    APP_PORT="$(find_available_port 8080 3000 18080 20080 || true)"

    if [[ -z "$APP_PORT" ]]; then
        error "未找到可用端口，请使用 --port 手动指定"
        exit 1
    fi

    warn "已切换到端口 $APP_PORT"
}

create_port_override_file() {
    PORT_OVERRIDE_FILE="$(mktemp)"
    TEMP_FILES+=("$PORT_OVERRIDE_FILE")

    cat >"$PORT_OVERRIDE_FILE" <<EOF
services:
  nginx:
    ports:
      - "${APP_PORT}:80"
EOF
}

create_image_override_file() {
    local backend_image="$1"
    local frontend_image="$2"

    IMAGE_OVERRIDE_FILE="$(mktemp)"
    TEMP_FILES+=("$IMAGE_OVERRIDE_FILE")

    cat >"$IMAGE_OVERRIDE_FILE" <<EOF
services:
  backend:
    image: ${backend_image}
  frontend:
    image: ${frontend_image}
EOF
}

has_real_value() {
    local key="$1"
    local value

    value="$(grep -E "^${key}=" "$ENV_FILE" | tail -n 1 | cut -d '=' -f 2- | tr -d '"' | tr -d '\r' || true)"

    if [[ -z "$value" ]]; then
        return 1
    fi

    case "$value" in
        your_*|sk-your-*|changeme|false)
            return 1
            ;;
        *)
            return 0
            ;;
    esac
}

print_env_hint() {
    if has_real_value "DEEPSEEK_API_KEY" || has_real_value "DASHSCOPE_API_KEY" || has_real_value "OPENAI_API_KEY" || has_real_value "GOOGLE_API_KEY"; then
        return
    fi

    warn "当前 .env 中还没有检测到可用的大模型 API Key"
    warn "Web 界面可以启动，但分析功能在配置密钥前无法正常使用"
}

wait_for_health() {
    local timeout_seconds=240
    local elapsed=0
    local health_url="http://127.0.0.1:${APP_PORT}/health"

    log "等待服务启动完成，最长 ${timeout_seconds} 秒"
    until curl -fsS "$health_url" >/dev/null 2>&1; do
        sleep 5
        elapsed=$((elapsed + 5))

        if (( elapsed >= timeout_seconds )); then
            error "服务启动超时，请执行以下命令查看日志："
            printf '  %s\n' "${COMPOSE_CMD[*]} -f docker-compose.hub.nginx.yml logs --tail=200"
            exit 1
        fi
    done
}

try_fast_start() {
    local backend_image="$1"
    local frontend_image="$2"

    log "尝试使用预构建镜像快速启动"
    log "后端镜像: $backend_image"
    log "前端镜像: $frontend_image"

    if ! docker pull "$backend_image"; then
        warn "后端镜像拉取失败"
        return 1
    fi

    if ! docker pull "$frontend_image"; then
        warn "前端镜像拉取失败"
        return 1
    fi

    create_image_override_file "$backend_image" "$frontend_image"

    compose \
        -f "$BASE_COMPOSE_FILE" \
        -f "$IMAGE_OVERRIDE_FILE" \
        -f "$PORT_OVERRIDE_FILE" \
        up -d --remove-orphans
}

build_start() {
    log "开始本地构建并启动，这通常比拉镜像慢一些"
    compose \
        -f "$BASE_COMPOSE_FILE" \
        -f "$PORT_OVERRIDE_FILE" \
        up -d --build --remove-orphans
}

main() {
    cd "$PROJECT_ROOT"

    log "TradingAgents-CN 一键启动"
    log "项目目录: $PROJECT_ROOT"

    resolve_compose_cmd
    require_prerequisites
    ensure_runtime_dirs
    ensure_env_file
    detect_arch
    ensure_port
    create_port_override_file
    print_env_hint

    if [[ "$FORCE_BUILD" == false ]]; then
        if [[ "$ARCH_SUFFIX" == "amd64" ]]; then
            if ! try_fast_start \
                "hsliuping/tradingagents-backend-amd64:latest" \
                "hsliuping/tradingagents-frontend-amd64:latest"; then
                warn "amd64 预构建镜像不可用，准备回退到本地构建"
                build_start
            fi
        elif [[ "$ARCH_SUFFIX" == "arm64" ]]; then
            if ! try_fast_start \
                "hsliuping/tradingagents-backend-arm64:latest" \
                "hsliuping/tradingagents-frontend-arm64:latest"; then
                warn "arm64 预构建镜像不可用，准备回退到本地构建"
                build_start
            fi
        else
            build_start
        fi
    else
        build_start
    fi

    wait_for_health

    printf '\n'
    log "启动完成"
    printf '访问地址: http://localhost:%s\n' "$APP_PORT"
    printf '健康检查: http://localhost:%s/health\n' "$APP_PORT"
    printf '停止服务: %s\n' "${COMPOSE_CMD[*]} -f docker-compose.hub.nginx.yml down"
    printf '查看日志: %s\n' "${COMPOSE_CMD[*]} -f docker-compose.hub.nginx.yml logs -f"
}

main "$@"
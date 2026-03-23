#!/usr/bin/env bash
# TradingAgents-CN 本地开发一键启动脚本
# 同时启动后端 (port 8000) 和前端 (port 3000)
# 用法: ./dev-start.sh  或  bash dev-start.sh

# 若用 sh 执行，自动切换为 bash
if [ -z "${BASH_VERSION:-}" ]; then
    exec bash "$0" "$@"
fi

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
BACKEND_LOG="$LOG_DIR/dev-backend.log"
FRONTEND_LOG="$LOG_DIR/dev-frontend.log"
BACKEND_PID_FILE="$PROJECT_ROOT/.dev-backend.pid"
FRONTEND_PID_FILE="$PROJECT_ROOT/.dev-frontend.pid"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

log()    { printf "${GREEN}[INFO]${NC} %s\n" "$1"; }
warn()   { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
error()  { printf "${RED}[ERROR]${NC} %s\n" "$1" >&2; }
header() { printf "\n${CYAN}========== %s ==========${NC}\n" "$1"; }

# 停止已有进程
stop_old() {
    for pidfile in "$BACKEND_PID_FILE" "$FRONTEND_PID_FILE"; do
        if [[ -f "$pidfile" ]]; then
            OLD_PID=$(cat "$pidfile" 2>/dev/null || true)
            if [[ -n "$OLD_PID" ]] && kill -0 "$OLD_PID" 2>/dev/null; then
                kill "$OLD_PID" 2>/dev/null && log "已停止旧进程 PID=$OLD_PID"
            fi
            rm -f "$pidfile"
        fi
    done
}

# 退出时清理
cleanup() {
    echo ""
    log "正在停止所有服务..."
    [[ -f "$BACKEND_PID_FILE" ]]  && kill "$(cat "$BACKEND_PID_FILE")"  2>/dev/null || true
    [[ -f "$FRONTEND_PID_FILE" ]] && kill "$(cat "$FRONTEND_PID_FILE")" 2>/dev/null || true
    rm -f "$BACKEND_PID_FILE" "$FRONTEND_PID_FILE"
    log "服务已停止"
}
trap cleanup EXIT INT TERM

# ── 检查依赖 ──────────────────────────────────────────────
header "环境检查"

# 在 venv 目录中查找可用的 Python 解释器（跳过损坏的符号链接）
_find_venv_python() {
    local venv_bin="$1/bin"
    for candidate in python3.13 python3.12 python3.11 python3.10 python3 python; do
        local p="$venv_bin/$candidate"
        # -f 对损坏符号链接返回 false，用 -e 也不行；直接执行测试
        if "$p" --version &>/dev/null 2>&1; then
            echo "$p"
            return 0
        fi
    done
    return 1
}

# Python 虚拟环境（优先使用已激活的 venv）
if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    VENV_PYTHON="$(_find_venv_python "$VIRTUAL_ENV" 2>/dev/null || true)"
    if [[ -n "$VENV_PYTHON" ]]; then
        log "使用已激活的虚拟环境: $VIRTUAL_ENV ($VENV_PYTHON)"
    fi
fi

if [[ -z "${VENV_PYTHON:-}" && -d "$PROJECT_ROOT/.venv" ]]; then
    VENV_PYTHON="$(_find_venv_python "$PROJECT_ROOT/.venv" 2>/dev/null || true)"
    if [[ -n "$VENV_PYTHON" ]]; then
        log "Python 虚拟环境: $VENV_PYTHON"
    fi
fi

if [[ -z "${VENV_PYTHON:-}" ]]; then
    error "未找到可用的虚拟环境，请先执行:"
    error "  python3 -m venv .venv && pip install -r requirements.txt"
    error "或先激活已有环境: source .venv/bin/activate"
    exit 1
fi

# 安装/补全后端依赖（pip 对已安装的包会快速跳过）
log "检查后端依赖..."
"$VENV_PYTHON" -m pip install \
    -r "$PROJECT_ROOT/requirements.txt" \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --quiet 2>&1 | grep -v "^$" || {
    error "依赖安装失败，请手动执行:"
    error "  $VENV_PYTHON -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"
    exit 1
}
log "后端依赖就绪"

# Node.js / npm
if ! command -v npm &>/dev/null; then
    error "未找到 npm，请先安装 Node.js"
    exit 1
fi
log "npm: $(npm --version)"

# .env 文件
if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
    if [[ -f "$PROJECT_ROOT/.env.example" ]]; then
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        warn "已从 .env.example 创建 .env，请检查并填写必要配置（API Key 等）"
    else
        error "未找到 .env 文件，请参考 docs/QUICK_START.md 创建"
        exit 1
    fi
fi

# MongoDB
if ! pgrep -x mongod &>/dev/null; then
    warn "MongoDB 未运行，尝试启动..."
    if command -v brew &>/dev/null && brew services list | grep -q "mongodb-community"; then
        brew services start mongodb-community 2>/dev/null && log "MongoDB 已通过 Homebrew 启动" || warn "MongoDB 启动失败，请手动启动"
    else
        warn "请手动启动 MongoDB (mongod)，否则后端可能报错"
    fi
fi

# Redis
if ! pgrep -x redis-server &>/dev/null; then
    warn "Redis 未运行，尝试启动..."
    if command -v brew &>/dev/null && brew services list | grep -q "redis"; then
        brew services start redis 2>/dev/null && log "Redis 已通过 Homebrew 启动" || warn "Redis 启动失败，请手动启动"
    else
        warn "请手动启动 Redis，否则后端可能报错"
    fi
fi

# ── 准备 ──────────────────────────────────────────────────
mkdir -p "$LOG_DIR"
stop_old

# 安装前端依赖（如果 node_modules 不存在）
if [[ ! -d "$PROJECT_ROOT/frontend/node_modules" ]]; then
    header "安装前端依赖"
    cd "$PROJECT_ROOT/frontend" && npm install
    cd "$PROJECT_ROOT"
fi

# ── 启动后端 ──────────────────────────────────────────────
header "启动后端"
cd "$PROJECT_ROOT"
"$VENV_PYTHON" -m app > "$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$BACKEND_PID_FILE"
log "后端已启动 PID=$BACKEND_PID，日志: $BACKEND_LOG"

# 等待后端就绪（最多 15 秒）
log "等待后端就绪..."
for i in $(seq 1 15); do
    if curl -sf http://localhost:8000/health &>/dev/null || \
       curl -sf http://localhost:8000/api/auth/status &>/dev/null || \
       curl -sf http://localhost:8000/docs &>/dev/null; then
        log "后端已就绪 (${i}s)"
        break
    fi
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        error "后端进程意外退出，查看日志: $BACKEND_LOG"
        tail -20 "$BACKEND_LOG"
        exit 1
    fi
    sleep 1
done

# ── 启动前端 ──────────────────────────────────────────────
header "启动前端"
cd "$PROJECT_ROOT/frontend"
npm run dev > "$FRONTEND_LOG" 2>&1 &
FRONTEND_PID=$!
echo "$FRONTEND_PID" > "$FRONTEND_PID_FILE"
log "前端已启动 PID=$FRONTEND_PID，日志: $FRONTEND_LOG"
cd "$PROJECT_ROOT"

# 等待前端就绪（最多 20 秒）
log "等待前端就绪..."
for i in $(seq 1 20); do
    if curl -sf http://localhost:3000 &>/dev/null; then
        log "前端已就绪 (${i}s)"
        break
    fi
    if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
        error "前端进程意外退出，查看日志: $FRONTEND_LOG"
        tail -20 "$FRONTEND_LOG"
        exit 1
    fi
    sleep 1
done

# ── 启动完成 ──────────────────────────────────────────────
header "启动完成"
printf "\n"
printf "  ${GREEN}前端地址:${NC}  http://localhost:3000\n"
printf "  ${GREEN}后端地址:${NC}  http://localhost:8000\n"
printf "  ${GREEN}API文档:${NC}   http://localhost:8000/docs\n"
printf "\n"
printf "  后端日志: tail -f $BACKEND_LOG\n"
printf "  前端日志: tail -f $FRONTEND_LOG\n"
printf "\n"
printf "  按 ${YELLOW}Ctrl+C${NC} 停止所有服务\n\n"

# 保持脚本运行，实时输出后端日志
tail -f "$BACKEND_LOG" &
wait "$BACKEND_PID" "$FRONTEND_PID"

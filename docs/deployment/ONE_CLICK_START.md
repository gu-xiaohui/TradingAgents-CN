# TradingAgents-CN 一键启动

这个脚本面向“换一台设备尽快跑起来”的场景，默认优先使用 Docker Hub 预构建镜像，拉取失败时自动回退到本地构建。

## 适用环境

- macOS
- Linux
- 已安装并启动 Docker

## 使用方式

在项目根目录执行：

```bash
chmod +x scripts/smart_start.sh
./scripts/smart_start.sh
```

首次运行如果没有 `.env`，脚本会自动从 `.env.example` 生成。

## 常用参数

```bash
# 指定访问端口
./scripts/smart_start.sh --port 8080

# 强制本地构建，不使用预构建镜像
./scripts/smart_start.sh --build
```

## 脚本行为

1. 检查 Docker 和 Compose 是否可用
2. 自动创建 `logs`、`data` 等运行目录
3. 自动初始化 `.env`
4. 自动检测 CPU 架构
5. 优先拉取对应架构的预构建镜像
6. 如果镜像不可用，自动回退到本地构建
7. 自动等待 `http://localhost:<port>/health` 健康检查通过

## 启动后访问

- 应用首页：`http://localhost:80`
- 如果 80 端口被占用，脚本会自动切换到其它空闲端口并打印实际地址

## 注意事项

- Web 页面能启动，不代表分析功能一定可用；分析前仍需在 `.env` 中配置至少一个大模型 API Key
- 如果你是在 Apple Silicon 设备上运行，脚本会优先拉取 arm64 镜像
- 如果公司网络无法访问 Docker Hub，脚本会自动尝试本地构建

## 故障排查

```bash
# 查看服务日志
docker compose -f docker-compose.hub.nginx.yml logs -f

# 停止服务
docker compose -f docker-compose.hub.nginx.yml down
```
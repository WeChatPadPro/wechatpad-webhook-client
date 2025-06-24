# WeChatPad Webhook Client

[![GitHub Repo](https://img.shields.io/badge/github-repo-blue?logo=github)](https://github.com/WeChatPadPro/wechatpad-webhook-client)

这是一个用于接收 [WeChatPadPro](https://github.com/WeChatPadPro) 推送消息的 Webhook 客户端，基于 Python 构建，支持签名验证、配置热加载、日志记录、消息重试及持久化，适用于需要集成微信消息推送的后端服务。

## ✨ 特性 Features

- 📬 接收 Webhook 推送
- 🔐 可选的签名验证机制
- 🔄 消息失败自动重试
- 🗃 SQLite 本地持久化
- 📝 日志输出支持
- ❤️ 心跳检测功能
- 🌐 WebSocket 支持（可选）

## 🚀 快速开始

```bash
git clone https://github.com/WeChatPadPro/wechatpad-webhook-client.git
cd wechatpad-webhook-client
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## ⚙️ 配置方式

你可以使用 `.env` 或 `data/config.json` 文件进行配置。支持以下环境变量：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `SERVER_HOST` | 0.0.0.0 | 监听地址 |
| `SERVER_PORT` | 8080 | Web 服务端口 |
| `WEBHOOK_PATH` | /webhook | 接收路径 |
| `SECRET_KEY` | 空 | 用于验证签名（可选） |
| `DB_PATH` | `data/webhook_messages.db` | 数据库存储路径 |
| `LOG_FILE` | `logs/webhook.log` | 日志文件路径 |
| `HEARTBEAT_INTERVAL` | 60 | 心跳检测间隔（秒） |
| `WS_ENABLED` | false | 启用 WebSocket（true/false） |
| `WS_URL` | 空 | WebSocket 服务地址 |

## 📡 Webhook 接口说明

- **URL**: `http://<SERVER_HOST>:<SERVER_PORT><WEBHOOK_PATH>`
- **方法**: `POST`
- **内容类型**: `application/json`
- **可选签名**: `X-Signature` 请求头，用于验证请求是否合法（需配置 `SECRET_KEY`）

### 示例 Payload

```json
{
  "type": "message",
  "from": "wxid_123456",
  "content": "Hello from WeChatPad"
}
```

## 📁 项目结构

```
wechatpad-webhook-client/
├── data/                  # 配置与数据库目录
├── logs/                  # 日志输出目录
├── main.py                # 主程序入口
├── config.py              # 配置管理模块
├── requirements.txt
└── .env.example           # 配置示例文件
```

## 🛠️ 贡献 Contributing

欢迎提交 PR 和 issue 来优化项目！

## 📝 License

本项目基于 MIT 协议开源。

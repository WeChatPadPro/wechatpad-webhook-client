# WeChatPad Webhook Server

一个用于接收 WeChatPad 消息推送的 Webhook 服务端，使用 Python 编写，支持配置热加载、签名验证、重试机制和日志记录，适用于需要对接微信消息的自动化系统。

## 特性 Features

- 📬 **Webhook 接收**：监听 HTTP 请求，接收 WeChatPad 推送的消息。
- 🔐 **签名验证**：支持配置 `SECRET_KEY` 进行请求验证（可选）。
- 🗃 **本地持久化**：使用 SQLite 存储消息记录。
- 🔄 **失败重试**：支持消息处理失败后的自动重试。
- 📂 **日志管理**：内建日志系统，输出详细的访问和错误日志。
- ❤️ **心跳检测**：定期向上游服务器发送心跳包（可选）。

## 快速开始 Quick Start

```bash
git clone https://github.com/yourname/wechatpad-webhook-server.git
cd wechatpad-webhook-server
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## 配置 Configuration

编辑 `.env` 文件或使用默认值：

| 环境变量 | 描述 | 默认值 |
|----------|------|--------|
| `SERVER_HOST` | Web 服务监听地址 | `0.0.0.0` |
| `SERVER_PORT` | Web 服务监听端口 | `8080` |
| `WEBHOOK_PATH` | Webhook 路径 | `/webhook` |
| `SECRET_KEY` | 请求签名密钥（可选） | 空 |
| `DB_PATH` | SQLite 数据库存储路径 | `data/webhook_messages.db` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `HEARTBEAT_INTERVAL` | 心跳包间隔（秒） | `60` |

## 接口说明 Webhook Endpoint

- **URL**: `http://<SERVER_HOST>:<SERVER_PORT><WEBHOOK_PATH>`
- **方法**: `POST`
- **内容类型**: `application/json`
- **签名校验**（可选）:
  - 客户端需在请求头中添加 `X-Signature`
  - 服务端通过 `SECRET_KEY` 进行验证

## 示例 Payload

```json
{
  "type": "message",
  "from": "user123",
  "content": "你好"
}
```

## License

MIT License

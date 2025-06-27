#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import hmac
import hashlib
import time
from datetime import datetime
import argparse
from flask import Flask, request, jsonify
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("webhook_client.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 全局配置
config = {
    "secret": "",  # webhook密钥，用于验证签名
    "verify_signature": False,  # 是否验证签名
    "save_messages": True,  # 是否保存消息到文件
    "message_file": "webhook_messages.json",  # 消息保存文件
    "print_messages": True,  # 是否打印消息内容
}

# 消息类型映射
MSG_TYPE_MAP = {
    1: "文本消息",
    3: "图片消息",
    34: "语音消息",
    43: "视频消息",
    47: "动画表情",
    49: "应用消息(文件、链接等)",
    10000: "系统提示"
}

# 验证签名
def verify_signature(secret, data, timestamp, signature):
    if not secret:
        return True
    
    # 计算签名: HMAC-SHA256(secret, timestamp + data)
    h = hmac.new(secret.encode(), digestmod=hashlib.sha256)
    h.update(str(timestamp).encode())
    h.update(data)
    calculated = h.hexdigest()
    
    return hmac.compare_digest(calculated, signature)

# 保存消息到文件
def save_message(message):
    try:
        # 读取现有消息
        try:
            with open(config["message_file"], "r", encoding="utf-8") as f:
                messages = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            messages = []
        
        # 添加新消息
        messages.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        })
        
        # 保存消息
        with open(config["message_file"], "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
            
        return True
    except Exception as e:
        logger.error(f"保存消息失败: {e}")
        return False

# Webhook接收端点
@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    start_time = time.time()
    
    # 获取请求数据
    data = request.get_data()
    timestamp = request.headers.get('X-Webhook-Timestamp')
    signature = request.headers.get('X-Webhook-Signature')
    
    # 记录请求信息
    logger.info(f"收到Webhook请求: timestamp={timestamp}, signature={signature}")
    
    # 验证签名
    if config["verify_signature"]:
        if not timestamp or not signature:
            logger.warning("请求缺少时间戳或签名")
            return jsonify({"success": False, "message": "缺少时间戳或签名"}), 400
        
        if not verify_signature(config["secret"], data, timestamp, signature):
            logger.warning("签名验证失败")
            return jsonify({"success": False, "message": "签名验证失败"}), 401
    
    # 解析JSON数据
    try:
        message = json.loads(data)
    except json.JSONDecodeError:
        logger.warning("无效的JSON数据")
        return jsonify({"success": False, "message": "无效的JSON数据"}), 400
    
    # 处理消息
    try:
        # 获取消息类型
        msg_type = message.get("msgType")
        msg_type_str = MSG_TYPE_MAP.get(msg_type, f"未知类型({msg_type})")
        
        # 获取发送者和接收者
        from_user = message.get("fromUser", "")
        to_user = message.get("toUser", "")
        
        # 获取消息内容
        content = message.get("content", "")
        
        # 打印消息信息
        if config["print_messages"]:
            logger.info(f"收到{msg_type_str}: {from_user} -> {to_user}")
            logger.info(f"内容: {content}")
        
        # 保存消息
        if config["save_messages"]:
            save_message(message)
        
        # 计算处理时间
        elapsed = (time.time() - start_time) * 1000  # 毫秒
        
        return jsonify({
            "success": True,
            "message": "消息已接收",
            "elapsed": elapsed
        })
    except Exception as e:
        logger.error(f"处理消息时出错: {e}")
        return jsonify({"success": False, "message": f"处理消息时出错: {e}"}), 500

# 主页
@app.route('/', methods=['GET'])
def home():
    return """
    <html>
        <head>
            <title>微信Webhook测试客户端</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                .info { background-color: #f0f0f0; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>微信Webhook测试客户端</h1>
            <div class="info">
                <p>这是一个用于接收微信Webhook消息的测试服务器。</p>
                <p>Webhook接收地址: <code>/webhook</code> (POST方法)</p>
                <p>当前状态: 正在运行</p>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='微信Webhook测试客户端')
    parser.add_argument('-p', '--port', type=int, default=8000, help='服务器端口 (默认: 8000)')
    parser.add_argument('-s', '--secret', type=str, default='', help='Webhook密钥')
    parser.add_argument('-v', '--verify', action='store_true', help='验证签名')
    parser.add_argument('-o', '--output', type=str, default='webhook_messages.json', help='消息保存文件')
    args = parser.parse_args()
    
    # 更新配置
    config["secret"] = args.secret
    config["verify_signature"] = args.verify
    config["message_file"] = args.output
    
    # 打印启动信息
    logger.info(f"启动Webhook测试客户端，监听端口: {args.port}")
    logger.info(f"验证签名: {'启用' if config['verify_signature'] else '禁用'}")
    logger.info(f"消息保存: {'启用，保存到 ' + config['message_file'] if config['save_messages'] else '禁用'}")
    
    # 启动服务器
    app.run(host='0.0.0.0', port=args.port, debug=False) 
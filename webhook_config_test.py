#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import argparse
import sys
import time

def config_webhook(base_url, key, webhook_url, secret, enabled=True, timeout=10, retry_count=3, 
                  message_types=None, include_self_message=True):
    """配置Webhook"""
    if message_types is None:
        message_types = ["1", "3", "34", "43", "47", "49"]  # 默认消息类型
    
    url = f"{base_url}/webhook/Config?key={key}"
    
    data = {
        "url": webhook_url,
        "secret": secret,
        "enabled": enabled,
        "timeout": timeout,
        "retryCount": retry_count,
        "messageTypes": message_types,
        "includeSelfMessage": include_self_message
    }
    
    print(f"正在配置Webhook: {webhook_url}")
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            print("Webhook配置成功!")
            return True
        else:
            print(f"Webhook配置失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"请求出错: {e}")
        return False

def test_webhook(base_url, key):
    """测试Webhook连通性"""
    url = f"{base_url}/webhook/Test?key={key}"
    
    print("正在测试Webhook连通性...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            data = result.get("data", {})
            success = data.get("Success", False)
            message = data.get("Message", "")
            elapsed = data.get("Elapsed", 0)
            
            if success:
                print(f"Webhook测试成功! 耗时: {elapsed}ms")
                return True
            else:
                print(f"Webhook测试失败: {message}")
                return False
        else:
            print(f"Webhook测试失败: {result.get('msg')}")
            return False
    except Exception as e:
        print(f"请求出错: {e}")
        return False

def get_webhook_status(base_url, key):
    """获取Webhook配置状态"""
    url = f"{base_url}/webhook/Status?key={key}"
    
    print("正在获取Webhook配置状态...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            data = result.get("data", {})
            print("\nWebhook配置状态:")
            print(f"URL: {data.get('url')}")
            print(f"启用状态: {'启用' if data.get('enabled') else '禁用'}")
            print(f"超时设置: {data.get('timeout')}秒")
            print(f"重试次数: {data.get('retryCount')}次")
            print(f"消息类型: {', '.join(data.get('messageTypes', []))}")
            print(f"包含自己的消息: {'是' if data.get('includeSelfMessage') else '否'}")
            print(f"最后发送时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get('lastSendTime', 0)))}")
            print(f"最后发送状态: {'成功' if data.get('lastSendStatus') else '失败'}")
            print(f"总发送成功: {data.get('totalSent', 0)}条")
            print(f"总发送失败: {data.get('totalFailed', 0)}条")
            return data
        else:
            print(f"获取Webhook状态失败: {result.get('msg')}")
            return None
    except Exception as e:
        print(f"请求出错: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='微信Webhook配置和测试工具')
    parser.add_argument('--url', type=str, required=True, help='微信API服务器地址')
    parser.add_argument('--key', type=str, required=True, help='微信API密钥')
    parser.add_argument('--action', type=str, choices=['config', 'test', 'status', 'all'], default='all', 
                        help='执行操作: config=配置, test=测试, status=状态, all=全部')
    
    # Webhook配置参数
    parser.add_argument('--webhook-url', type=str, help='Webhook接收地址')
    parser.add_argument('--secret', type=str, default='', help='Webhook密钥')
    parser.add_argument('--enable', type=bool, default=True, help='是否启用Webhook')
    parser.add_argument('--timeout', type=int, default=10, help='请求超时时间(秒)')
    parser.add_argument('--retry', type=int, default=3, help='失败重试次数')
    parser.add_argument('--types', type=str, default='1,3,34,43,47,49', 
                        help='消息类型,逗号分隔(1=文本,3=图片,34=语音,43=视频,47=表情,49=应用消息)')
    parser.add_argument('--include-self', type=bool, default=True, help='是否包含自己发送的消息')
    
    args = parser.parse_args()
    
    # 检查参数
    if args.action in ['config', 'all'] and not args.webhook_url:
        print("错误: 配置Webhook需要指定--webhook-url参数")
        sys.exit(1)
    
    # 解析消息类型
    message_types = args.types.split(',') if args.types else []
    
    # 执行操作
    if args.action in ['config', 'all']:
        success = config_webhook(
            args.url, args.key, args.webhook_url, args.secret,
            args.enable, args.timeout, args.retry, 
            message_types, args.include_self
        )
        if not success and args.action == 'all':
            print("配置失败，停止后续操作")
            sys.exit(1)
        print()
    
    if args.action in ['status', 'all']:
        get_webhook_status(args.url, args.key)
        print()
    
    if args.action in ['test', 'all']:
        test_webhook(args.url, args.key)

if __name__ == "__main__":
    main() 
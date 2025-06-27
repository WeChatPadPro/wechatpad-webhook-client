# 微信Webhook測試工具

這個專案包含兩個Python腳本，用來測試微信Webhook功能：
1. `webhook_client_test.py`: Webhook接收伺服器，用於接收和處理微信發送的webhook訊息
2. `webhook_config_test.py`: Webhook設定工具，用於設定和測試webhook連接

## 前提條件

- Python 3.6+
- 安裝所需依賴：
 『`bash
 pip install flask requests
 ```

## 使用方法

### 1. 啟動Webhook接收伺服器

『`bash
python webhook_client_test.py -p 8000 -s your_secret_key -v
```

參數說明：
- `-p, --port`: 伺服器連接埠號，預設為8000
- `-s, --secret`: Webhook金鑰，用於驗證簽名
- `-v, --verify`: 是否驗證簽名
- `-o, --output`: 訊息儲存文件，預設為webhook_messages.json

啟動後，伺服器將監聽在 `http://你的IP位址:8000/webhook`

### 2. 設定Webhook

『`bash
python webhook_config_test.py --url http://微信API伺服器位址 --key 你的微信API金鑰 --webhook-url http://你的IP位址:8000/webhook --secret your_secret_key
```

參數說明：
- `--url`: 微信API伺服器位址
- `--key`: 微信API金鑰
- `--action`: 執行操作，可選值：config(配置)、test(測試)、status(狀態)、all(全部)，預設為all
- `--webhook-url`: Webhook接收位址
- `--secret`: Webhook金鑰
- `--enable`: 是否啟用Webhook，預設為True
- `--timeout`: 請求超時時間(秒)，預設為10
- `--retry`: 失敗重試次數，預設為3
- `--types`: 訊息類型，逗號分隔，預設為1,3,34,43,47,49
- `--include-self`: 是否包含自己發送的訊息，預設為True

### 3. 查看接收到的訊息

Webhook接收伺服器會將接收到的訊息保存在 `w​​ebhook_messages.json` 檔案中，同時也會在控制台和日誌檔案 `webhook_client.log` 中輸出訊息內容。

## 訊息類型參考

| 類型值 | 說明 |
|-------|------|
| 1 | 文字訊息 |
| 3 | 圖片訊息 |
| 34 | 語音訊息 |
| 43 | 視訊訊息 |
| 47 | 動畫表情 |
| 49 | 應用程式訊息（檔案、連結等） |
| 10000 | 系統提示 |

## 完整測試流程範例

1. 啟動Webhook接收伺服器：
 『`bash
 python webhook_client_test.py -p 8000 -s mysecretkey
 ```

2. 設定Webhook並測試連通性：
 『`bash
 python webhook_config_test.py --url http://微信API伺服器位址 --key 你的微信API金鑰 --webhook-url http://你的公用IP:8000/webhook --secret mysecretkey
 ```

3. 傳送一則微信訊息，然後查看webhook_messages.json檔案或webhook_client.log日誌，確認是否收到訊息。

## 注意事項

1. 確保你的伺服器可以從外網訪問，或使用內網穿透工具（如ngrok）將本地伺服器暴露到公網
2. 如果使用簽章驗證，確保設定Webhook時的secret與啟動接收伺服器時的secret一致
3. 如果無法接收訊息，請檢查：
 - 伺服器防火牆是否開放了對應端口
 - Webhook配置的URL是否正確
 - 網路連線是否正常
 - 查看日誌檔排查問題

## 調試技巧

1. 使用 `--action status` 查看Webhook設定狀態：
 『`bash
 python webhook_config_test.py --url http://微信API伺服器位址 --key 你的微信API金鑰 --action status
 ```

2. 使用 `--action test` 測試Webhook連通性：
 『`bash
 python webhook_config_test.py --url http://微信API伺服器位址 --key 你的微信API金鑰 --action test
 ```

3. 若在內網環境測試，可以使用ngrok等工具進行內網穿透：
 『`bash
 ngrok http 8000
 ```
 然後使用ngrok提供的公網URL作為we​​bhook-url

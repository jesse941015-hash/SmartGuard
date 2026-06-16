# SmartGuard 智慧門禁與雲端防盜系統

這是一個基於 Raspberry Pi 5 與 LINE Messaging API 的無鑰匙外宿防盜監控系統。當門磁感測器偵測到大門被異常開啟時，系統會在本地觸發蜂鳴器，並即時發送 LINE 推播通知給遠端使用者。

## 硬體接線配置 (Hardware Setup)
* **主控板**: Raspberry Pi 5
* **門磁感測器 (Door Sensor)**: 兩端分別接至 **GPIO 23** 與 **GND**。
* **蜂鳴器 (Buzzer - 低電平觸發)**: 訊號線接至 **GPIO 21**，VCC 與 GND 依模組標示連接。

## 系統環境建置 (Installation)
請在終端機依序執行以下指令，建立獨立的虛擬環境並安裝必要套件：

1. 建立專案資料夾與虛擬環境：
```bash
mkdir SmartGuard
cd SmartGuard
python -m venv venv --system-site-packages
source venv/bin/activate
```

2. 安裝核心 Python 套件：
```bash
pip install requests python-dotenv gpiozero
```

## 環境變數設定 (Configuration)
為了保護資安，本專案使用 `.env` 管理金鑰。
1. 請複製根目錄下的 `.env.example` 並重新命名為 `.env`：
```bash
cp .env.example .env
```

2. 開啟 `.env` 檔案，並填入你從 LINE Developers 後台取得的憑證：
```env
LINE_CHANNEL_ACCESS_TOKEN=你的長期_Channel_Access_Token
LINE_USER_ID=你的_User_ID
```

## 系統執行 (Usage)
確認硬體接線與 `.env` 設定無誤後，執行以下指令啟動系統：
```bash
python smartguard_test.py
```
* **系統待命**：程式將顯示「等待感測器訊號...」。
* **觸發警報**：將門磁感測器拉開，本地蜂鳴器將鳴叫，手機 LINE 會收到警告通知。
* **警報解除**：將門磁感測器重新靠攏，蜂鳴器停止，手機 LINE 會收到恢復通知。
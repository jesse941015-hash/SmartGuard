#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
from dotenv import load_dotenv
from gpiozero import Button, LED
from signal import pause

# 載入 .env 內的環境變數
load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")
PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/push"

# 【修正 1】過濾金屬彈跳
door_sensor = Button(23, pull_up=True, bounce_time=0.3)

# 【修正 3】加上 active_high=False，專門對付「低電平觸發」的蜂鳴器！
alarm_buzzer = LED(21, active_high=False)

def send_text_message(to: str, text: str) -> None:
    """呼叫 LINE Push API 送出文字訊息"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    }
    body = {
        "to": to,
        "messages": [{"type": "text", "text": text}],
    }
    resp = requests.post(PUSH_ENDPOINT, headers=headers, json=body, timeout=10)
    if resp.status_code != 200:
        print("送出失敗, status:", resp.status_code)
    else:
        print("已送出 LINE 訊息:", text)

def trigger_alarm():
    """當大門拉開時觸發"""
    print("⚠️ 偵測到大門開啟！觸發警報！")
    alarm_buzzer.on() # 因為設定了 active_high=False，這裡會輸出低電位讓蜂鳴器響起
    send_text_message(USER_ID, "⚠️ SmartGuard 警告：大門遭到異常開啟！請立即確認！")

def stop_alarm():
    """當大門靠近時觸發"""
    print("大門狀態恢復。")
    alarm_buzzer.off() # 輸出高電位，蜂鳴器停止
    send_text_message(USER_ID, "✅ SmartGuard 通知：大門已重新關閉，警報解除。")

def main():
    if not CHANNEL_ACCESS_TOKEN or not USER_ID:
        print("請先在 .env 中設定 LINE_CHANNEL_ACCESS_TOKEN 和 LINE_USER_ID")
        sys.exit(1)

    # 【修正 2】符合門磁感測器的物理特性
    door_sensor.when_released = trigger_alarm  # 磁鐵拉開 (斷路) -> 觸發警報
    door_sensor.when_pressed = stop_alarm      # 磁鐵靠近 (導通) -> 停止警報

    print("第 10 組 SmartGuard 系統啟動中...")
    print("等待感測器訊號... (按 Ctrl+C 結束程式)")
    
    # 確保系統啟動時，蜂鳴器是安靜的
    alarm_buzzer.off()
    
    try:
        pause()
    except KeyboardInterrupt:
        print("\n系統關閉中...")
        alarm_buzzer.off()

if __name__ == "__main__":
    main()
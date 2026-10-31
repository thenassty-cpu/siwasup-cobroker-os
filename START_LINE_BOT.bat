@echo off
chcp 65001 >nul
title Siwasup LINE OA Bot (@813nyyia) Auto-Tunnel & Chat Logger
cd /d "C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
echo ============================================================================
echo [Siwasup LINE OA] Starting Gemini Webhook + Auto-Tunnel + Real-time Logger
echo Monitor Dashboard: https://assets.siwasup.com/line_chat_monitor.html
echo ============================================================================
python scripts\start_line_bot_daemon.py
pause

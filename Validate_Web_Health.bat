@echo off
chcp 65001 >nul
title Siwasup Web Health Validator
color 0B

echo ==============================================================================
echo    Siwasup Co-Broker OS - Web Health Validator
echo ==============================================================================
echo.

python "%~dp0scripts\validate_web.py"

echo.
echo ==============================================================================
echo กดปุ่มใดก็ได้เพื่อปิดหน้าต่างนี้...
pause >nul

@echo off
title EnergyWise - konsol demo
chcp 65001 >nul
mode con cols=90 lines=40
cd /d "%~dp0.."
".venv\Scripts\python.exe" app.py

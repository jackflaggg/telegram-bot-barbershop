@echo off

call %~dp0tgbot\venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN=5327606415:AAG_4Dyh7sJuxvCAnRi0e6O_koLM1lN2ARs

python bot_telegram.py

pause
@echo off
clear
mkdir dist 2>nul
mkdir dist\icon 2>nul
copy .\icon\app_icon.png dist\icon\app_icon.png 2>nul
copy config.toml dist 2>nul
copy system.toml dist 2>nul

"python.exe" "..\python\Scripts\pyinstaller.exe" --noconsole --onefile --clean --icon=".\icon\app_icon.ico" "main.pyw"

rd /S /Q __pycache__
rd /S /Q build
del main.spec

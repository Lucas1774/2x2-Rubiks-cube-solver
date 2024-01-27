@echo off
pyinstaller --onefile src\solver.py
move dist\solver.exe .
rmdir /s /q dist
rmdir /s /q build
del solver.spec
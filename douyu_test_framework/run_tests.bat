@echo off
REM Windows批处理脚本 - 运行测试

echo ========================================
echo Douyu Test Framework - Test Runner
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM 切换到脚本目录
cd /d "%~dp0"

REM 运行测试
echo Running tests...
python run_tests.py %*

echo.
echo ========================================
echo Test execution completed
echo ========================================
pause

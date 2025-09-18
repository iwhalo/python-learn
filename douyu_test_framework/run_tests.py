#!/usr/bin/env python
"""主测试运行脚本"""
import sys
import os
import subprocess
from pathlib import Path


def setup_environment():
    """设置测试环境"""
    # 将项目根目录添加到Python路径
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # 创建必要的目录
    directories = ["screenshots", "logs", "test-results", "videos"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✓ Environment setup complete")


def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False
    
    # 安装Playwright浏览器
    print("Installing Playwright browsers...")
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], 
                      check=True)
        print("✓ Playwright browsers installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install browsers: {e}")
        return False
    
    return True


def run_tests(args=None):
    """运行pytest测试"""
    print("\n" + "="*60)
    print("Starting Douyu Test Framework Execution")
    print("="*60 + "\n")
    
    # 获取项目根目录
    root_dir = Path(__file__).parent
    
    # 默认pytest参数
    pytest_args = [
        "-v",
    ]
    
    # 检查pytest-html是否已安装
    try:
        import pytest_html
        # 创建报告目录(使用绝对路径)
        report_dir = root_dir / "test-results"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # 使用绝对路径作为报告路径
        report_path = report_dir / "report.html"
        pytest_args.extend([f"--html={report_path}", "--self-contained-html"])
        print(f"HTML report will be saved to: {report_path}")
    except ImportError:
        print("Note: pytest-html not installed, HTML report will not be generated")
    
    # 添加自定义参数（如果提供）
    if args:
        pytest_args.extend(args)
    
    # 运行pytest
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest"] + pytest_args,
            cwd=Path(__file__).parent
        )
        return result.returncode
    except Exception as e:
        print(f"✗ Test execution failed: {e}")
        return 1


def main():
    """主入口点"""
    # 切换到脚本目录
    os.chdir(Path(__file__).parent)
    
    print("Douyu Test Framework")
    print("=" * 60)
    
    # 设置环境
    setup_environment()
    
    # 检查是否需要安装依赖
    if "--install" in sys.argv or not Path("requirements.txt").exists():
        if not install_dependencies():
            sys.exit(1)
        sys.argv = [arg for arg in sys.argv if arg != "--install"]
    
    # 运行测试
    additional_args = sys.argv[1:] if len(sys.argv) > 1 else []
    exit_code = run_tests(additional_args)
    
    print("\n" + "="*60)
    print("Test Execution Complete")
    print("="*60)
    print(f"Exit Code: {exit_code}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

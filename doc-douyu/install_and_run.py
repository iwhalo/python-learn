"""
安装依赖并运行斗鱼文档抓取器
"""
import subprocess
import sys
import os


def install_requirements():
    """安装依赖"""
    print("正在安装依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装完成!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False


def run_scraper():
    """运行抓取器"""
    print("正在运行斗鱼文档抓取器...")
    try:
        subprocess.check_call([sys.executable, "scraper.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"运行抓取器失败: {e}")
        return False


def main():
    print("斗鱼文档抓取器 - 安装和运行工具")
    print("="*50)
    
    # 更改到当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 安装依赖
    if not install_requirements():
        print("由于依赖安装失败，程序退出")
        return False
    
    # 运行抓取器
    if run_scraper():
        print("\n抓取器运行完成!")
        return True
    else:
        print("\n抓取器运行失败!")
        return False


if __name__ == "__main__":
    main()
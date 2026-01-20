"""
用于修复Git问题的Python脚本
解决本地与远程分支分歧及文件删除问题
"""

import os
import subprocess
import sys


def run_command(cmd):
    """
    执行命令行命令
    """
    try:
        print(f"执行命令: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        result = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            capture_output=True,
            text=True,
            check=True
        )
        print("输出:", result.stdout.strip())
        if result.stderr:
            print("错误:", result.stderr.strip())
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None


def fix_git_issues():
    """
    修复Git问题的主要函数
    """
    print("开始修复Git问题...")
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")
    
    # 1. 获取远程更新
    print("\n1. 获取远程更新...")
    run_command(["git", "fetch", "origin"])
    
    # 2. 查看状态
    print("\n2. 查看当前状态...")
    run_command(["git", "status"])
    
    # 3. 强制重置到远程主分支（谨慎操作）
    print("\n3. 尝试硬重置到远程状态...")
    local_result = run_command(["git", "rev-parse", "HEAD"])
    remote_result = run_command(["git", "rev-parse", "origin/master"])
    
    if local_result and remote_result and local_result != remote_result:
        print("本地和远程提交不同，尝试合并...")
        # 先尝试正常拉取
        pull_result = run_command(["git", "pull", "origin", "master"])
        if pull_result is None:
            # 如果正常拉取失败，尝试rebase
            print("正常拉取失败，尝试rebase...")
            run_command(["git", "rebase", "origin/master"])
    else:
        print("本地和远程已经是同一状态")
    
    # 4. 检查是否还有未跟踪的文件
    print("\n4. 检查未跟踪的__pycache__目录...")
    status_output = run_command(["git", "status", "--porcelain"])
    if status_output:
        print("发现未跟踪的文件/目录:")
        print(status_output)
        
        # 删除所有 __pycache__ 目录
        import shutil
        for root, dirs, files in os.walk("."):
            for d in dirs:
                if d == "__pycache__":
                    pycache_path = os.path.join(root, d)
                    print(f"删除 {pycache_path}")
                    try:
                        shutil.rmtree(pycache_path)
                    except Exception as e:
                        print(f"删除失败: {e}")
    
    # 5. 再次检查状态
    print("\n5. 最终检查状态...")
    run_command(["git", "status"])
    
    print("\nGit问题修复完成！")


if __name__ == "__main__":
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    fix_git_issues()
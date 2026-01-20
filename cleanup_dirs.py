"""
清理不需要的目录和文件
"""
import os
import shutil

def cleanup_directories():
    """清理特定目录"""
    base_path = "D:\\PycharmProjects\\python-learn"
    
    # 要删除的目录模式
    dirs_to_remove = []
    
    # 收集所有 __pycache__ 目录
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            if d == "__pycache__":
                dirs_to_remove.append(os.path.join(root, d))
    
    # 也尝试删除可能存在的 logs 目录
    logs_path = os.path.join(base_path, "wedding_invitation", "logs")
    if os.path.exists(logs_path):
        dirs_to_remove.append(logs_path)
    
    # 删除收集到的目录
    for dir_path in dirs_to_remove:
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                print(f"已删除目录: {dir_path}")
            else:
                print(f"目录不存在: {dir_path}")
        except Exception as e:
            print(f"删除目录 {dir_path} 时出错: {e}")
    
    print("清理完成!")

if __name__ == "__main__":
    cleanup_directories()
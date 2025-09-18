import os
import requests


def resume_download(url, save_path):
    """支持断点续传的文件下载函数"""
    headers = {}
    downloaded_size = 0

    # 检查文件是否已经存在（断点续传）
    if os.path.exists(save_path):
        downloaded_size = os.path.getsize(save_path)
        headers['Range'] = f'bytes={downloaded_size}-'
        print(f"Resuming from {downloaded_size} bytes")

    # 创建请求
    r = requests.get(url, headers=headers, stream=True)

    # 如果是断点续传，服务器应返回 206 Partial Content
    if downloaded_size > 0 and r.status_code == 206:
        mode = 'ab'  # 追加模式
    else:
        mode = 'wb'  # 覆盖模式
        downloaded_size = 0

    # 获取总文件大小
    total_size = int(r.headers.get('content-length', 0)) + downloaded_size

    # 下载文件
    with open(save_path, mode) as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
                progress = downloaded_size / total_size if total_size > 0 else 0
                print(f"\rProgress: {progress:.2%} of {total_size} bytes", end="")
    print("\nDownload complete!")


# 使用示例
resume_download('https://example.com/large.zip', 'large.zip')
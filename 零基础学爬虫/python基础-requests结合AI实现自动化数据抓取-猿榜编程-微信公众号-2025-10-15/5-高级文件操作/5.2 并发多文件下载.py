import concurrent.futures
import os
import requests


def download_file(url, save_path, session=None):
    """下载单个文件并保存到指定路径"""
    s = session or requests.Session()
    r = s.get(url, stream=True)
    r.raise_for_status()

    # 获取文件总大小
    total_size = int(r.headers.get('content-length', 0))

    # 创建目录（如果不存在）
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 下载文件
    downloaded = 0
    with open(save_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            downloaded += len(chunk)
            f.write(chunk)
            progress = downloaded / total_size if total_size > 0 else 0
            print(f"\r{save_path}: {progress:.2%}", end="", flush=True)
    print()  # 打印换行
    return save_path


# 并发下载多个文件
files_to_download = [
    ('https://example.com/file1.zip', 'downloads/file1.zip'),
    ('https://example.com/file2.pdf', 'downloads/file2.pdf'),
    # 更多文件...
]

# 使用线程池执行并发下载
with requests.Session() as session:
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(download_file, url, path, session)
            for url, path in files_to_download
        ]

        # 获取结果（可能会抛出异常）
        for future in concurrent.futures.as_completed(futures):
            try:
                path = future.result()
                print(f"Successfully downloaded: {path}")
            except Exception as e:
                print(f"Download failed: {e}")
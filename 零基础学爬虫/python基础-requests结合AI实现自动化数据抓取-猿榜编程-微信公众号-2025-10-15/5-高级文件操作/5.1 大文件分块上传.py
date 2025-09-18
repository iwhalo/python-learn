import requests

# 采用分块传输编码（chunked transfer encoding）上传大文件
def file_generator(file_path, chunk_size=8192):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# 使用生成器实现流式上传
file_path = 'large_video.mp4'
headers = {'Transfer-Encoding': 'chunked'}
r = requests.post(
    'https://httpbin.org/post',
    data=file_generator(file_path),
    headers=headers
)

import urllib.request
import uuid
import mimetypes

def upload_file(url,file_path,field_name='file'):
    # 生成分隔符
    boundary=str(uuid.uuid4())

    # 获取文件名和MIME类型
    file_name=file_path.split('/')[-1]
    content_type=mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

    # 读取文件内容
    with open(file_path,'rb') as f:
        file_data=f.read()

    # 构建multipart/form-data请求体
    data=[]
    data.append(f'--{boundary}'.encode())
    data.append(f'Content-Disposition:form-data;name="{field_name}";filename="{file_name}"'.encode())
    data.append(f'Content-Type:{content_type}'.encode())
    data.append(b'')
    data.append(file_data)
    data.append(f'--{boundary}--'.encode())
    data.append(b'')

    body=b'\r\n'.join(data)

    # 创建请求
    req=urllib.request.Request(
        url=url,
        data=body
    )

    # 设置Content-Type
    req.add_header('Content-Type',f'multipart/form-data;boundary={boundary}')
    req.add_header('Content-Length',str(len(body)))

    # 发送请求
    response=urllib.request.urlopen(req)

    return response.read().decode('utf-8')


if __name__ == '__main__':
    result=upload_file(
        url='http://httpbin.org/post',
        file_path='test.jpg',
    )
    print(result)
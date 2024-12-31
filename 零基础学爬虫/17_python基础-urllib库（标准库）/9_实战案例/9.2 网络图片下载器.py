import urllib.request
import urllib.parse
import urllib.error
import os
import re
import time
import random


class ImageDownloader:
    def __init__(self,save_dir='images'):
        self.save_dir=save_dir
        os.makedirs(save_dir,exist_ok=True)

        # 创建opener
        self.opener=urllib.request.build_opener()
        self.opener.addheaders=[
            ('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'),
            ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
            ('Accept-Language','en-US,en;q=0.5'),
            ('Connection','keep-alive')
        ]
        # 安装opener作为默认
        urllib.request.install_opener(self.opener)

    def download_image(self,img_url,filename=None):
        """下载单个图片"""
        try:
            # 生成文件名
            if not filename:
                filename=os.path.basename(urllib.parse.urlparse(img_url).path)
                if not filename or '.' not in filename:
                    filename=f"image_{int(time.time())}_{random.randint(1000,9999)}.jpg"

                # 完整保存路径
                save_path=os.path.join(self.save_dir,filename)

                # 下载图片
                # print(f"下载图片：{img_url} -> {save_path}")
                # urllib.request.urlretrieve(img_url,save_path)

                # # 使用opener下载图片
                # response=self.opener.open(img_url,timeout=10)
                # with open(save_path,'wb') as f:
                #     f.write(response.read())
                # print(f"下载图片：{img_url} -> {save_path}")

                # 下载图片
                print(f"下载图片：{img_url} -> {save_path}")
                # 创建请求对象并添加headers
                req=urllib.request.Request(img_url)
                req.add_header(
                    'User-Agent',self.opener.addheaders[0][1]
                )
                # 下载文件
                with urllib.request.urlopen(req) as response,open(save_path,'wb') as out_file:
                    out_file.write(response.read())

                return save_path
        except Exception as e:
            print(f"下载失败：{e}")
            return None

    def extract_images_from_page(self,page_url):
        """从网页中提取图片URL"""
        try:
            # 获取页面内容
            # response=self.opener.open(page_url,timeout=10)
            # html=response.read().decode('utf-8')

            req=urllib.request.Request(page_url)
            req.add_header(
                'User-Agent',self.opener.addheaders[0][1])
            with urllib.request.urlopen(req) as response:
                html=response.read().decode('utf-8')

            # 提取图片URL，同时匹配src和data-src属性
            img_pattern=r'<img[^>]+src=[\'"]([^\'"]+)[\'"]'
            # img_pattern=r'<img[^>]+(?:src|data-src)=[\'"]([^\'"]+)[\'"]'
            # img_urls=[]
            img_urls=set()  # 使用集合避免重复

            for match in re.finditer(img_pattern,html):
                img_url=match.group(1)
                # 转换为绝对URL
                absolute_url=urllib.parse.urljoin(page_url,img_url)
                # img_urls.append(absolute_url)
                img_urls.add(absolute_url)


            return img_urls

        except Exception as e:
            print(f"提取图片失败：{e}")
            return []

    def batch_download(self,img_urls,delay=1):
        """批量下载图片"""
        success_count=0
        fail_count=0

        for i,img_url in enumerate(img_urls):
            result=self.download_image(img_url)

            if result:
                success_count+=1
            else:
                fail_count+=1

            # 添加延迟
            if i<len(img_urls)-1 and delay>0:
                time.sleep(delay)

        print(f"下载完成：成功 {success_count} 张，失败 {fail_count} 张")
        return success_count,fail_count

    def download_from_page(self,page_url,delay=1):
        """从网页下载所有图片"""
        # 提取图片URL
        img_urls=self.extract_images_from_page(page_url)
        print(f"找到 {len(img_urls)} 张图片")

        # 批量下载
        return self.batch_download(img_urls,delay)

#     使用示例
if __name__ == '__main__':
    downloader=ImageDownloader('downloaded_images')
    # 从页面下载图片
    # downloader.download_from_page(page_url='https://pixnio.com/zh/%25E6%25A0%2587%25E7%25AD%25BE/%e5%85%8d%e8%b4%b9%e5%9b%be%e7%89%87')

    # 下载单个图片
    downloader.download_image('https://www.python.org/static/img/python-logo.png')


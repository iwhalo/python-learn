import threading
import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor

from typing import List,Tuple

from Crypto.SelfTest.Cipher.test_CFB import file_name
from django.db.models.expressions import result

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s-%(threadName)s-%(levelName)s-%(message)s'
)
logger=logging.getLogger(__name__)

class DownloadManager:
    """文件下载管理器，支持多线程并行下载"""
    def __init__(self,max_workers:int=5):
        """
        初始化下载管理器
        参数：
            max_workers：最大工作线程数
        """
        self.max_workers=max_workers

        # 使用线程池管理线程资源
        self.executor=ThreadPoolExecutor(max_workers=self.max_workers,thread_name_prefix="Downloader")
    def download_file(self,file_name:str,url:str,timeout:int=30)->bool:
        """
        下载单个文件的方法：
        参数：
            file_name：保存的文件名字
            url：下载文件的url地址
            timeout：请求超时时间（秒）
        返回：
            bool：下载是否成功
        """
        try:
            logger.info(f"开始下载 {file_name}")
            start_time=time.time()

            # 添加请求头，模拟浏览器行为
            headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            }

            # 使用超时和流式下载 处理大文件
            with requests.get(url=url,headers=headers,stream=True,timeout=timeout) as response:
                # 确保请求成功
                response.raise_for_status()
                # 获取文件大小（如果服务器提供）
                total_size=int(response.headers.get('content-length',0))

                with open(file_name,'wb') as f:
                    # 分快下载，避免一次性加载大文件到内存
                    chunk_size=8192 # 8kb
                    downloaded=0
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        # 过滤保持链接活跃得空块
                        if chunk:
                            f.write(chunk)
                            downloaded+=len(chunk)

                            # 记录下载进度
                            if total_size>0:
                                progress=(downloaded/total_size)*100
                            if downloaded%(5*chunk_size)==0: # 每下载约40KB更新一次进度
                                logger.debug(f"{file_name} - 下载进度：{progress:.1f}%")
                elapsed=time.time()-start_time
                logger.info(f"{file_name} 下载完成 - 耗时：{elapsed:.2f}秒")
                return True
        except requests.exceptions.RequestException as e:
            logger.error(f"下载 {file_name} 失败：{str(e)}")
            return False
        except IOError as e:
            logger.error(f"文件处理错误 {file_name}：{str(e)}")
            return False
        except Exception as e:
            logger.error(f"下载 {file_name} 时发生未知错误：{str(e)}")
            return False

    def download_multiple(self,url_list:List[Tuple[str,str]])->List[bool]:
        """
        并行下载多个文件
        参数：
            url_list:包含（文件名，URL）元组的列表
        返回：
            List[bool]:每个下载任务的成功状态列表
        """

        logger.info(f"开始下载 {len(url_list)} 个文件，使用 {self.max_workers} 个线程")

        # 提交所有下载任务到线程池
        futures=[
            self.executor.submit(self.download_file,file_name,url) for file_name,url in url_list
        ]

        # 等待所有任务完成并收集结果
        results=[]
        for future in futures:
            try:
                result=future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"执行任务时发生异常：{str(e)}")
                results.append(False)

        # 统计成功率
        success_count=sum(results)
        logger.info(f"所有下载任务完成！成功：{success_count}/{len(url_list)}")

        return results

    def shutdown(self):
        """关闭线程池，释放资源"""
        self.executor.shutdown(wait=True)
        logger.info("下载管理器已关闭")


if __name__ == '__main__':
    # 测试URL列表
    url_list=[
        ("video1.mp4","https://example.com/video1"),
        ("video2.mp4","https://example.com/video2"),
        ("video3.mp4","https://example.com/video3")
    ]

    # 创建下载管理器，并开始下载
    downloader=DownloadManager(max_workers=3)
    try:
        results=downloader.download_multiple(url_list)
    finally:
    #     确保资源被正确释放
        downloader.shutdown()




import asyncio
import logging
import os
import time

import aiofiles
import aiohttp

from aiohttp import ClientSession
from typing import List,Tuple,Dict,Any



# 配置日志
def get_logger(name=None):
    logger=logging.getLogger(name)
    if not logger.handlers:
        handler=logging.StreamHandler()
        formatter=logging.Formatter(
            '%(asctime)s - %(processName)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
logger=get_logger(__name__)

"""
异步HTTP下载器，基于aiohttp和asyncio实现
"""
class AsyncDownloader:

    """
    初始化下载器
    参数：
        download_dir：下载文件保存目录
        chunk_size：下载时的块大小（字节）
    """
    def __init__(self,download_dir:str="./downloads",chunk_size:int=8192):
        self.download_dir=download_dir
        self.chunk_size=chunk_size

        # 确保下载目录存在
        os.makedirs(download_dir,exist_ok=True)
        logger.info(f"异步下载器初始化完成，下载目录：{download_dir}")

    """
    异步下载单个文件
    参数：
        session：aiohttp会话对象
        url：下载url
        file_name：保存的文件名
    返回：
        Dict：下载结果信息
    """
    async def download_file(self,session:ClientSession,url:str,filename:str)->Dict[str,Any]:
        file_path=os.path.join(self.download_dir,filename)
        start_time=time.time()

        # 记录下载信息
        result={
            'url':url,
            'file_name':file_name,
            'file_path':file_path,
            'success':False,
            'file_size':0,
            'download_time':0,
            'speed':0,
            'error':None
        }

        try:
            logger.info(f"开始下载：{file_name} 从{url}")

            # 发送请求并流式下载
            async with session.get(url,ssl=False) as response:
                if response.status!=200:
                    error_msg=f"HTTP错误：{response.status} - {response.reason}"
                    logger.error(error_msg)
                    result['error']=error_msg

                    return result

                # 获取文件大小（如果服务器提供）
                content_length=response.headers.get('Content-Length')
                if content_length:
                    total_size=int(content_length)
                    result['file_size']=total_size
                    logger.info(f"{file_name} 大小：{total_size/1024:.2f} KB")

                # 异步写入文件
                async with aiofiles.open(file_path,'wb') as f:
                    downloaded=0
                    last_log_time=time.time()

                    # 流式下载，避免内存溢出
                    async for chunk in response.content.iter_chunked(self.chunk_size):
                        await f.write(chunk)
                        downloaded+=len(chunk)
                        # 每秒最多记录一次进度
                        current_time=time.time()
                        if current_time-last_log_time>=1.0 and total_size>0:
                            progress=(downloaded/total_size)*100
                            logger.debug(f"{file_name} - 下载进度：{progress:.1f}%")
                            last_log_time=current_time

            # 计算下载统计信息
            download_time=time.time()-start_time
            speed=result['file_size']/download_time if download_time>0 else 0

            result.update({
                'success':True,
                'download_time':download_time,
                'speed':speed
            })

            logger.info(f"{file_name} 下载完成 - 耗时：{download_time:.2f} 秒 - 速度：{speed/1024:.1f} KB/s")

            return result

        except aiohttp.ClientError as e:
            error_msg=f"网络错误：{str(e)}"
            logger.error(f"下载 {file_name} 失败：{error_msg}")
            result['error']=error_msg

            return result

        except asyncio.CancelledError:
            error_msg="下载被取消"
            logger.warning(f"{file_name} 下载被取消")
            result['error']=error_msg

            return result

        except Exception as e:
            error_msg=f"未知错误：{str(e)}"
            logger.error(f"下载 {file_name} 时发生异常：{error_msg}")
            result['error']=error_msg

            return result


    """
    批量并发下载多个文件
    参数：
        urls：包含（文件名，URL）元组的列表
        max_concurrent：最大并发下载数
    返回：
        List[Dict]：下载结果列表
    """
    async def download_batch(self,urls:List[Tuple[str,str]],max_concurrent:int=5)->List[Dict[str,Any]]:
        if not urls:
            logger.warning("没有提供下载URL")
            return []

        logger.info(f"开始批量下载 {len(urls)} 个文件，最大并发数 {max_concurrent}")

        start_time=time.time()
        # 创建限制并发数的信号量
        semaphore=asyncio.Semaphore(max_concurrent)

        # 定义带信号量的下载函数
        async def bounded_download(session,file_name,url):
            async with semaphore:
                return await self.download_file(session,url,file_name)

        # 创建会话并发送请求
        async with aiohttp.ClientSession() as session:
            # 创建所有下载任务
            tasks=[
                bounded_download(session,file_name,url)
                for file_name,url in urls
            ]

            # 并发执行所有任务
            results=await asyncio.gather(*tasks,return_exceptions=True)

        # 处理结果
        processed_results=[]
        success_count=0

        for result in results:
            # 检查是否发生异常
            if isinstance(result,Exception):
                logger.error(f"下载任务异常：{str(result)}")
                processed_results.append({
                    'success':False,
                    'error':str(result)
                })
            else:
                processed_results.append(result)
                if result['success']:
                    success_count+=1

        # 统计信息
        total_time=time.time()-start_time
        success_rate=(success_count/len(urls))*100 if urls else 0
        logger.info(f"批量下载完成！总耗时：{total_time:.2f} 秒")
        logger.info(f"成功：{success_count}/{len(urls)} ({success_rate:.1f}%)")

        return processed_results

"""
主函数
"""
async def main():
    # 创建下载器实例
    downloader=AsyncDownloader(download_dir="./downloads")

    # 准备下载列表（替换为实际可用的URL）
    urls=[
        ('image1.jpg','https://example.com/image1.jpg'),
        ('image2.jpg','https://example.com/image2.jpg'),
        ('image3.jpg','https://example.com/image3.jpg'),
        ("document1.pdf","https://example.com/document1.pdf"),
        ("document2.pdf","https://example.com/document2.pdf")
    ]

    # 开始批量下载
    results=await downloader.download_batch(urls,max_concurrent=3)

    # 打印下载结果摘要
    print("\n下载结果摘要")
    for result in results:
        if result.get('success'):
            file_name=result.get('file_name')
            size_kb=result.get('file_size',0)/1024
            time_s=result.get('download_time',0)
            speed_kbps=result.get('speed',0)/1024
            print(f"✅ {file_name}：{size_kb:.1f} KB，{time_s:.2f} 秒，{speed_kbps:.1f} KB/s")
        else:
            url=result.get('url','Unknown URL')
            error=result.get('error','Unknown error')
            print(f"❌ {url}: {error}")

if __name__ == '__main__':
    # 在Python 3.7+中可以直接使用asyncio.run()
    asyncio.run(main())
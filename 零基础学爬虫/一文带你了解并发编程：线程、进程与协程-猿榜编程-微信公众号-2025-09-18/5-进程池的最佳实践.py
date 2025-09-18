import logging
import multiprocessing as mp
import time
from typing import List,Tuple,Dict,Any

from concurrent.futures import ProcessPoolExecutor

import random

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

# 使用方式
logger=get_logger(__name__)

class AdvancedTaskProcessor:
    """高级任务处理器，演示进程池最佳实践"""
    def __init__(self,max_workers:int=None):
        """
        初始化处理器
        参数：
            max_workers：最大工作进程数，默认为CPU核心数
        """
        self.max_workers=max_workers or mp.cpu_count()
        logger.info(f"初始化高级任务处理器，最大进程数：{self.max_workers}")

    def process_single_task(self,task_data:Tuple[int,int])->Tuple[int,float]:
        """
        处理单个任务的函数
        参数：
            task_data：任务数据，格式为（任务ID，任务复杂度）

        返回：
            Tuple[int,float]：（任务ID，处理结果）
        """
        task_id,complexity=task_data
        process_id=mp.current_process().pid

        logger.info(f"进程 {process_id} 开始处理任务 {task_id}，复杂度：{complexity}")

        # 模拟计算密集型工作
        start_time=time.time()
        # 根据任务复杂度决定计算量
        iterations=complexity*1000000
        result=0
        for i in range(iterations):
            result+=i%10
            # 避免过度优化
            if i%1000000==0:
                result=result*0.99999

        # 计算处理时间
        processing_time=time.time()-start_time

        logger.info(f"进程 {process_id} 完成任务 {task_id}，耗时：{processing_time:.2f} 秒")

        return task_id,result

    def process_tasks_with_pool(self,tasks:List[Tuple[int,int]])->List[Tuple[int,float]]:
        """
        使用进程池处理多个任务
        参数：
            tasks：任务列表，每个任务为（任务ID，任务复杂度）元组
        返回：
            List[Tuple[int,float]]：处理结果列表
        """
        logger.info(f"开始处理 {len(tasks)} 个任务，使用 {self.max_workers} 个进场")

        start_time=time.time()

        results=[]

        # 使用ProcessPoolExecutor进行并行处理
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            futures=[executor.submit(self.process_single_task,task) for task in tasks]

            # 收集结果
            for future in futures:
                try:
                    result=future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"任务执行出错：{str(e)}")

        elapsed=time.time()-start_time
        logger.info(f"所有任务处理完成，总耗时：{elapsed:.2f} 秒")

        return results

    def run_demo(self,num_tasks:int=10,seed:int=42):
        """
        运行演示
        参数：
            num_tasks：任务数量
            seed：随机种子，确保可重复性
        """
        random.seed(seed)

        # 创建任务列表，复杂度在1到5之间随机
        tasks=[(i,random.randint(1,5)) for i in range(num_tasks)]

        logger.info(f"创建了 {num_tasks} 个子任务")
        logger.info(f"任务列表：{tasks}")

        # 处理任务
        results=self.process_tasks_with_pool(tasks)

        # 输出结果
        logger.info(f"处理结果：{results}")

if __name__ == '__main__':
    processor=AdvancedTaskProcessor()
    processor.run_demo(num_tasks=8)



import asyncio
import logging
import random
import time
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

"""基于协程的异步任务管理器"""
class AsyncTaskManager:

    """初始化异步任务管理器"""
    def __init__(self):
        logger.info("初始化异步任务管理器")
        self.results={}

    """
    模拟一个异步任务
    参数：
        task_id：任务ID
        duration：模拟的任务执行时间（秒）
    返回：
        Dict：任务结果数据
    """
    async def task_simulator(self,task_id:int,duration:float)->Dict[str,Any]:
        logger.info(f"任务 {task_id} 开始，预计耗时：{duration:.2f} 秒")

        # 模拟不同任务阶段
        stages=['初始化','数据加载','处理中','完成']

        result_data={
            'task_id':task_id,
            'stages':{},
            'total_time':0
        }

        start_time=time.time()

        # 分阶段执行任务
        stage_time=duration/len(stages)
        for i,stage in enumerate(stages):
            # 模拟每个阶段的工作
            stage_start=time.time()
            # 使用asyncio.sleep模拟异步IO操作
            variation=random.uniform(0.8,1.2) # 增加一些随机性
            await asyncio.sleep(stage_time*variation)
            stage_duration=time.time()-stage_start
            result_data['stages'][stage]=stage_duration

            logger.debug(f"任务 {task_id} : {stage} 阶段完成，耗时 {stage_duration:.2f} 秒")

        # 计算总耗时
        total_time=time.time()-start_time
        result_data['total_time']=total_time

        logger.info(f"任务 {task_id} 完成，总耗时 {total_time:.2f} 秒")
        return result_data

    """
    并发运行多个异步任务
    参数：
        num_tasks:任务数量
        min_duration：最小任务持续时间
        max_duration：最大任务持续时间
    返回：
        List[Dict]：所有任务结果列表
    """
    async def run_tasks(self,num_tasks:int=5,min_duration:float=1.0,max_duration:float=5.0)->List[Dict[str,Any]]:
       logger.info(f"准备运行 {num_tasks} 个异步任务")

       # 生成随机任务持续时间
       durations=[random.uniform(min_duration,max_duration) for _ in range(num_tasks)]

       # 创建任务列表
       tasks=[
           self.task_simulator(i,durations[i]) for i in range(num_tasks)
       ]

       # 并发执行所有任务
       start_time=time.time()
       results=await asyncio.gather(*tasks)
       total_time=time.time()-start_time

       # 分析结果
       theoretical_sequential_time=sum(durations)
       speedup=theoretical_sequential_time/total_time
       logger.info(f"所有任务完成。总耗时：{total_time:.2f} 秒")
       logger.info(f"如果顺序执行，预计需要：{theoretical_sequential_time:.2f} 秒")
       logger.info(f"加速比：{speedup:.2f}x")

       return results

"""
主函数
"""
async def main():
    manager=AsyncTaskManager()

    # 运行并发任务
    results=await manager.run_tasks(num_tasks=10,min_duration=1.0,max_duration=3.0)

    # 输出结果摘要
    print("\n任务执行摘要：")
    for result in results:
        task_id=result['task_id']
        total_time=result['total_time']
        print(f"任务 {task_id} : 总耗时：{total_time:.2f} 秒")

if __name__ == '__main__':
    # 在Python 3.7+中，可以直接使用asyncio.run()
    asyncio.run(main())
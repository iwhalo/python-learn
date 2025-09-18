import multiprocessing as mp
import time
import logging
import os
import math
from platform import processor
from typing import List, Tuple, Dict, Any

# 配置日志
"""
常用的日志记录属性包括：

%(name)s - 记录器名称

%(levelname)s - 日志级别名称（小写）

%(levelno)s - 日志级别数字

%(pathname)s - 源文件路径

%(filename)s - 文件名

%(module)s - 模块名

%(funcName)s - 函数名

%(lineno)d - 行号

%(message)s - 日志消息
"""
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# 使用更健壮的日志配置
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

class ParallelProcessor:
    """并行任务处理器，基于多进程执行"""

    def __init__(self, num_processes: int = None):
        """
        初始化并行处理器
        参数：
            num_processes：进程数量，默认为CPU的核心数
        """
        # 若未指定进程数，则使用CPU核心数
        self.num_processes = num_processes or mp.cpu_count()
        logger.info(f"初始化并行处理器，使用 {self.num_processes} 个进程")

    def _worker_calc_partial_sum(self, task_id: int, start: int, end: int, result_queue: mp.Queue) -> None:
        """
        工作进程函数：计算部分和
        参数：
            task_id：任务id
            start：起始值（包含）
            end：结束值（包含）
            result_queue：结果队列
        """
        try:
            process_id = os.getpid()
            logger.info(f"任务 {task_id} 开始于进程 {process_id} ，计算范围：[{start},{end}]")
            # 用数学公式计算区间和，比循环更高效
            # sum(range(start,end)) = (end - 1 + start) * (end - start) / 2
            result = (end - 1 + start) * (end - start) // 2
            # 也可以用内置sum函数，但在特大范围时可能效率较低
            # result = sum(range(start,end))

            # 将结果放入队列
            result_queue.put((task_id, result))
            logger.info(f"任务 {task_id} 完成，结果：{result}")
        except Exception as e:
            logger.error(f"任务 {task_id} 出错：{str(e)}")
            # 放入错误结果
            result_queue.put((task_id, None))

    def calculate_sum(self, start: int, end: int) -> int:
        """
        并行计算从start到end-1的整数和
        参数：
            start：起始值（包含）
            end：结束值（包含）
        返回：
            int：计算结果
        """
        if end <= start:
            return 0
        # 创建通信队列
        result_queue = mp.Queue()

        # 计算每个进程的工作量
        total_range = end - start
        chunk_size = math.ceil(total_range / self.num_processes)

        # 创建进程列表
        processes = []
        logger.info(f"开始计算从 {start} 到 {end} 的和，分为 {self.num_processes} 个子任务")
        start_time = time.time()

        # 创建并自启动所有进程
        for i in range(self.num_processes):
            task_start = start + i * chunk_size
            task_end = min(task_start + chunk_size, end)
            # 若已超出范围，跳过创建进程
            if task_start >= end:
                continue

            p = mp.Process(
                target=self._worker_calc_partial_sum,
                args=(i, task_start, task_end, result_queue),
                name=f"Calculator-{i}"
            )
            processes.append(p)
            p.start()

        # 收集结果
        results = {}
        for _ in range(len(processes)):
            task_id, value = result_queue.get()
            if value is not None:
                results[task_id] = value

        # 等待所有进程结束
        for p in processes:
            p.join()

        # 检查是否所有任务都成功完成
        if len(results) != len(processes):
            logger.warning(f"部分任务失败！只收到 {len(results)}/{len(processes)} 个结果")

        # 计算总和
        total_sum = sum(results.values())
        elapsed = time.time() - start_time
        logger.info(f"计算完成！耗时：{elapsed:.2f} 秒")
        logger.info(f"结果：{total_sum}")

        return total_sum


# 验证函数，确认并行计算结果正确性
def verify_sum(start: int, end: int, result: int) -> bool:
    """验证计算结果是否正确"""
    # 使用数学公式计算正确答案
    expected = (end - 1 + start) * (end - start) // 2
    logger.info(f"验证结果 - 计算值：{result}，期望值：{expected}")
    return result == expected


if __name__ == '__main__':
    # 计算从0到1亿的和
    START = 0
    END = 100_000_000

    processor = ParallelProcessor()
    result = processor.calculate_sum(START, END)
    # 验证结果
    is_correct = verify_sum(START, END, result)
    print(f"\n计算结果：{result}")
    print(f"\n结果验证：{'✓ 正确' if is_correct else '✗ 错误'}")

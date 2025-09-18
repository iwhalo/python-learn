import multiprocessing as mp
import logging
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

class ShareDataProcessor:
    """演示多进程间数据共享的处理器"""
    def __init__(self):
        """初始化处理器"""
        logger.info("初始化共享数据处理器")

    def using_value_and_array(self):
        """使用共享内存Value和Array的示例"""
        # 创建共享整数和数组
        shared_counter=mp.Value('i',0) # 'i'表示有符号整数
        shared_array=mp.Array('d',[0.0]*5) # 'd'表示双精度浮点数
        processes=[]

        # 定义工作函数
        def worker(counter,array,worker_id):
            pid=mp.current_process().pid
            logger.info(f"工作进程 {worker_id} (PID：{pid}) 开始")

            # 修改共享计数器
            with counter.get_lock():
                counter.value+=1
                logger.info(f"工作进程 {worker_id} 增加计数器值到 {counter.value}")
            # 修改共享内存
            with array.get_lock():
                for i in range(len(array)):
                    array[i]=array[i]+worker_id
                logger.info(f"工作进程 {worker_id} 更新数组：{list(array)}")
            logger.info(f"工作进程 {worker_id} 完成")

        # 创建并启动进程
        for i in range(3):
            p=mp.Process(
                target=worker,
                args=(shared_counter,shared_array,i)
            )
            processes.append(p)
            p.start()

        # 等待进程完成
        for p in process:
            p.join()

        logger.info(f"所有进程完成。最终计数器值：{shared_counter.value}")
        logger.info(f"所有进程完成。最终数组值：{list(shared_array)}")

    def using_manager(self):
        """使用Manager共享复杂数据结构示例"""
        # 创建Manager对象
        with mp.Manager() as manager:
            # 创建共享字典和列表
            shared_dict=manager.dict()
            shared_list=manager.list()

            # 创建共享锁
            lock=manager.RLock()
            processes=[]

            # 定义工作函数
            def worker(shared_dict,shared_list,lock,worker_id):
                pid=mp.current_process().pid
                logger.info(f"工作进程 {worker_id} （PID：{pid}）开始")

                # 安全地修改共享字典
                with lock:
                    shared_dict[f'key_{worker_id}']=worker_id*worker_id
                    shared_dict['total']=shared_dict.get('total',0)+worker_id
                    logger.info(f"工作进程 {worker_id} 更新字典：{dict(shared_dict)}")

                # 安全地修改共享列表
                with lock:
                    shared_list.append(f"来自进程 {worker_id} 的数据")
                    logger.info(f"工作进程 {worker_id} 更新列表：{list(shared_list)}")

                # 模拟一些工作
                time.sleep(0.5)
                logger.info(f"工作进程 {worker_id} 完成")

            # 创建并自启动进程
            for i in range(5):
                p=mp.Process(
                    target=worker,
                    args=(shared_dict,shared_list,lock,i),
                    name=f"Manager-Worker-{i}"
                )
                processes.append(p)
                p.start()

            # 等待进程完成
            for p in processes:
                p.join()

            logger.info("所有进程完成")
            logger.info(f"最终共享字典：{dict(shared_dict)}")
            logger.info(f"最终共享列表：{list(shared_list)}")

if __name__ == '__main__':
    processor=ShareDataProcessor()
    print("\n== 使用 Value 和 Array 共享数据 ==")
    processor.using_value_and_array()

    print("\n== 使用 Manager 共享数据 ==")
    processor.using_manager()







"""
运行以上代码会报错：
这个错误是因为在 Windows 系统上使用 multiprocessing 时，子进程无法正确序列化局部函数。

错误原因：

Windows 使用 spawn 方式创建进程，需要序列化所有数据到子进程

局部函数（在另一个函数内部定义的函数）无法被正确序列化

Python 的 pickle 模块无法处理局部函数

解决方案要点：

将函数定义为模块级或类方法：确保函数在全局作用域可访问

使用 if __name__ == "__main__"：防止子进程重复执行主模块代码

考虑使用进程池：multiprocessing.Pool 提供了更简洁的接口

推荐使用解决方案 1：将 worker 函数定义为类方法或模块级函数，因为它保持了代码的面向对象结构，同时解决了序列化问题。
"""
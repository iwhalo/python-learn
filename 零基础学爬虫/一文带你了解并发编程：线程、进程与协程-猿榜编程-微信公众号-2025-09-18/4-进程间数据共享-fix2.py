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

    # 定义工作函数
    @staticmethod
    def value_array_worker(counter, array, worker_id):
        """Value和Array的工作函数 - 静态方法"""
        pid = mp.current_process().pid
        logger.info(f"工作进程 {worker_id} (PID：{pid}) 开始")

        # 修改共享计数器
        with counter.get_lock():
            counter.value += 1
            logger.info(f"工作进程 {worker_id} 增加计数器值到 {counter.value}")

        # 修改共享内存
        with array.get_lock():
            for i in range(len(array)):
                array[i] = array[i] + worker_id
            logger.info(f"工作进程 {worker_id} 更新数组：{list(array)}")
        logger.info(f"工作进程 {worker_id} 完成")

    # 定义工作函数
    @staticmethod
    def manager_worker(shared_dict, shared_list, lock, worker_id):
        """Manager的工作函数 - 静态方法"""
        pid = mp.current_process().pid
        logger.info(f"工作进程 {worker_id} （PID：{pid}）开始")

        # 安全地修改共享字典
        with lock:
            shared_dict[f'key_{worker_id}'] = worker_id * worker_id
            shared_dict['total'] = shared_dict.get('total', 0) + worker_id
            logger.info(f"工作进程 {worker_id} 更新字典：{dict(shared_dict)}")

        # 安全地修改共享列表
        with lock:
            shared_list.append(f"来自进程 {worker_id} 的数据")
            logger.info(f"工作进程 {worker_id} 更新列表：{list(shared_list)}")

        # 模拟一些工作
        time.sleep(0.5)
        logger.info(f"工作进程 {worker_id} 完成")


    def using_value_and_array(self):
            """使用共享内存Value和Array的示例"""
            # 创建共享整数和数组
            shared_counter=mp.Value('i',0) # 'i'表示有符号整数
            shared_array=mp.Array('d',[0.0]*5) # 'd'表示双精度浮点数
            processes=[]

            # 创建并启动进程
            for i in range(3):
                p=mp.Process(
                    target=self.value_array_worker,
                    args=(shared_counter,shared_array,i)
                )
                processes.append(p)
                p.start()

            # 等待进程完成
            for p in processes:
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

            # 创建并自启动进程
            for i in range(5):
                p=mp.Process(
                    target=self.manager_worker,
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

如果您希望将工作函数保留在类内部，可以使用静态方法：

主要修改点
将静态方法移到类级别：将 @staticmethod 装饰器移到类的方法定义层面，而不是在方法内部定义

正确调用静态方法：在创建进程时使用 self.value_array_worker 和 self.manager_worker

保持代码结构：所有功能逻辑保持不变，只是调整了方法的定义位置

关键区别说明
静态方法 vs 局部函数：

❌ 错误：在方法内部定义函数并使用 @staticmethod

✅ 正确：在类级别定义静态方法

为什么这样能工作：

静态方法是类的一部分，可以被正确序列化

在 Windows 的 spawn 模式下，子进程能够导入模块并访问这些静态方法

使用 self.static_method 实际上是通过实例访问静态方法，这是完全有效的
"""
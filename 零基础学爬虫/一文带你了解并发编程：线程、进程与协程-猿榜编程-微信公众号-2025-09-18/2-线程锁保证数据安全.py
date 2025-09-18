import threading
import logging
import time


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
)

logger=logging.getLogger(__name__)

class ThreadSafeCounter:
    """线程安全的计数器实现"""
    def __init__(self,initial_value:int=0):
        """
        初始化计数器
        参数：
            initial_value：计数器初始值
        """
        self._value=initial_value
        self._lock=threading.RLock()   # 可重入锁，支持同一线程多次获取

    def increment(self,amount:int=1)->int:
        """
        增加计数器值  并返回新值
        参数：
            amount：增加的数量
        返回：
            int：增加后的计数器值
        """
        with self._lock:
            self._value+=amount
            current=self._value
        return current

    def decrement(self,amount:int=1)->int:
        """
        减少计数器值 并返回新值
        参数：
            amount：减少的数量
        返回：
            int：减少后的计数器值
        """
        with self._lock:
            self._value-=amount
            current=self._value
        return current

    @property
    def value(self)->int:
        """
        获取当前计数器值
        返回：
            int：当前计数器值
        """
        with self._lock:
            return self._value

def worker(counter:ThreadSafeCounter,iterations:int,worker_id:int):
    """
    工作线程函数，执行指定次数计数器增加操作
    参数：
    counter：线程安全的计数器对象
    iterations：迭代次数
    worker_id：工作线程ID
    """
    logger.info(f"工作线程 {worker_id} 开始执行")

    for i in range(iterations):
        # 模拟一些随机工作量
        if i%10000==0:
            logger.debug(f"工作线程 {worker_id} 已完成 {i} 次操作")
        # 增加计数器
        counter.increment()

    logger.info(f"工作线程 {worker_id} 完成，共执行 {iterations} 此操作")

def run_threaded_counter_test(num_threads:int=5,iterations_per_thread:int=100000):
    """
    运行多线程计数器测试
    参数：
        num_threads：线程数量
        iterations_per_thread：每个线程执行的迭代次数
    """
    # 创建线程安全计数器
    counter=ThreadSafeCounter()

    # 创建线程列表
    threads:List[threading.Thread]=[]
    logger.info(f"开始测试：{num_threads} 个线程，每个线程 {iterations_per_thread} 此操作")
    start_time=time.time()

    # 创建并启动所有线程
    for i in range(num_threads):
        t=threading.Thread(
            target=worker,
            args=(counter,iterations_per_thread,i),
            name=f"Worker-{i}"
        )
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    elapsed=time.time()-start_time


    # 验证结果
    expected=num_threads*iterations_per_thread
    actual=counter.value

    logger.info(f"测试完成！耗时：{elapsed:.2f} 秒")
    logger.info(f"计数器最终值：{actual}")
    logger.info(f"期望值：{expected}")
    logger.info(f"结果{'正确' if actual==expected else '不正确'}")

if __name__ == '__main__':
    run_threaded_counter_test(num_threads=5,iterations_per_thread=100000)

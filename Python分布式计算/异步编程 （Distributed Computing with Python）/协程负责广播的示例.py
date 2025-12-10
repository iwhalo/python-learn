# 定义了一个装饰器函数，用于将普通生成器函数转换为协程。协程在启动时会自动执行到第一个yield处等待数据。
def coroutine(fn):
    def wrapper(*args, **kwargs):  # 这是装饰器内部的定义函数，它接受任意位置参数和关键字参数。
        c = fn(*args, **kwargs)  # 调用被装饰的函数（生成器函数）创建一个生成器对象。
        next(c)  # 启动生成器，使其运行到第一个yield表达式处暂停。
        return c  # 返回这个生成器对象（即协程）。

    return wrapper  # 返回包装函数。


#  定义了一个函数，它读取文件中的每一行，并发送给子协程（child）
def cat(f, case_insensitive, child):
    """
    f: 文件对象
    case_insensitive: 是否忽略大小写
    child: 子协程，用于接收处理后的行
    """
    #  判断是否忽略大小写。
    if case_insensitive:
        line_processor = lambda l: l.lower()  # 如果忽略大小写，则定义一个lambda函数将字符串转换为小写。
    else:
        line_processor = lambda l: l  # 否则，定义一个什么都不做的lambda函数（原样返回）。

    for line in f:  # 遍历文件的每一行。
        child.send(line_processor(line))  # 将处理后的行（可能转换为小写）发送给子协程。


# 应用coroutine装饰器到grep函数上，使其成为协程。
# 定义grep协程，用于在文本中查找子字符串，并将出现的次数发送给子协程。
@coroutine
def grep(substring, case_insensitive, child):
    """
    substring: 要查找的子字符串
    case_insensitive: 是否忽略大小写
    child: 子协程，用于接收计数
    """
    #  判断是否忽略大小写。
    if case_insensitive:
        substring = substring.lower()  # 如果忽略大小写，将子字符串转换为小写。
    while True:  # 无限循环，等待接收文本。
        text = (yield)  # 接收从上游发送来的文本。
        child.send(text.count(substring))  # 计算子字符串在文本中出现的次数，并发送给子协程。


# 应用coroutine装饰器到counter函数上。
# 定义counter协程，用于累加次数并在协程结束时打印结果。
@coroutine
def counter(substring):
    """
    substring: 模式字符串，用于在结束时打印
    """
    n = 0  # 初始化计数器。
    try:  # 开始try块，用于捕获GeneratorExit异常。
        while True:  # 无限循环，等待接收数字（次数）。
            n += (yield)#  接收一个数字并累加到n。
    except GeneratorExit:# 当协程被关闭时（即没有更多数据发送，调用close()时）会抛出GeneratorExit异常。
        print(substring, n)# 打印模式字符串和出现的总次数。


#  应用coroutine装饰器到fanout函数上。
#  定义fanout协程，用于将接收到的数据广播给多个子协程。参数：
@coroutine
def fanout(children):
    """
    children: 子协程列表
    """
    while True:# 无限循环，等待接收数据。
        data = (yield) #  接收数据。
        for child in children: # 将数据发送给每一个子协程。
            child.send(data)
            """
            将接收到的数据同时发送给多个子协程
            实现了一对多的数据分发模式
            """


if __name__ == '__main__':
    import argparse# 导入argparse模块，用于解析命令行参数。

    parser = argparse.ArgumentParser()#  创建参数解析器。
    parser.add_argument('-i', action='store_true', dest='case_insensitive')# 添加一个布尔选项-i，当出现时表示忽略大小写，存储到case_insensitive变量。
    parser.add_argument('patterns', type=str, nargs='+', )# 添加位置参数patterns，表示一个或多个模式字符串。
    parser.add_argument('infile', type=argparse.FileType('r'))# 添加位置参数infile，表示输入文件，以只读方式打开。

    args = parser.parse_args()#  解析命令行参数。

    # 构建协程管道
    cat(args.infile,
        args.case_insensitive,
        fanout([grep(p,  # 为每个模式创建 grep 协程
                     args.case_insensitive,
                     counter(p))  # 每个 grep 连接一个 counter
                for p in args.patterns]))

"""
这是主调用：

首先，对于args.patterns中的每一个模式p，创建一个grep协程，该协程忽略大小写取决于args.case_insensitive，并且其子协程是counter(p)（用于计数该模式）。

然后，将这些grep协程放入一个列表，传递给fanout，创建一个广播协程。

最后，调用cat函数，传入文件对象、是否忽略大小写和广播协程。

这样，cat函数读取文件的每一行，处理大小写后发送给fanout，fanout将每一行广播给每一个grep协程。grep协程在每一行中查找自己的子字符串，并将出现的次数发送给对应的counter协程。counter协程累加次数，当所有行处理完后，cat函数结束，fanout协程也会被关闭，然后grep协程和counter协程依次关闭。当counter协程关闭时（收到GeneratorExit异常），打印出模式字符串和总次数。

注意：在cat函数处理完所有行后，程序并没有显式关闭各个协程。实际上，当cat函数结束时，fanout协程还在等待数据，而grep和counter也在等待。但是由于没有更多数据发送，它们会一直挂起，直到程序结束。但是counter协程的GeneratorExit异常是如何触发的呢？实际上，当程序结束时，这些生成器对象会被垃圾回收，这会调用生成器的close()方法，从而触发GeneratorExit异常。因此，在程序退出前，counter协程会打印出结果。

但是，更规范的做法是显式关闭这些协程。不过在这个例子中，由于cat函数是数据的生产者，它处理完文件后，整个管道就没有数据了，所以我们可以认为这些协程的任务已经完成。程序结束时会自动清理。

但是，如果cat函数后面还有其他的操作，那么这些协程可能会一直存在。所以，一个更好的做法是在cat函数结束后，显式关闭这些协程。但在这个例子中，由于cat函数是最后一步，所以没有显式关闭。

让我们看一下代码的流程：

打开文件，读取每一行。

对每一行，根据是否忽略大小写进行转换。

将转换后的行发送给fanout协程。

fanout协程将这一行发送给多个grep协程（每个模式一个）。

每个grep协程在行中查找自己的子字符串，并将出现的次数发送给对应的counter协程。

counter协程累加次数。

文件读取完毕后，cat函数结束。

程序结束，counter协程被关闭，打印结果。

注意：counter协程是在grep协程之后创建的，并且作为grep协程的子协程。grep协程在每次收到一行时，都会发送一个数字（出现次数）给counter协程。counter协程累加这些数字。

另外，fanout协程的作用是将每一行数据广播给多个grep协程。这样，每一行都会被所有的模式同时检查。

整个程序的结构是一个生产者-消费者模型，cat是生产者，counter是最终的消费者，而grep和fanout是中间的处理者。它们通过send方法传递数据，形成一个处理管道。
"""



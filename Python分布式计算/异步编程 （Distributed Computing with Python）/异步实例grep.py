
"""
1. 协程装饰器
作用：自动预激协程，避免每次使用时都要手动调用next()
示例：@coroutine装饰的函数会自动执行到第一个yield语句处暂停
"""
def coroutine(fn):
    def wrapper(*args, **kwargs):
        c = fn(*args, **kwargs) # 1. 调用原始函数，创建生成器对象
        next(c)                 # 2. 预激（prime）生成器，执行到第一个yield
        return c                # 3. 返回已预激的生成器
    return wrapper

"""
2. cat函数 - 文件读取器

"""
def cat(f, case_insensitive, child):
    if case_insensitive:
        line_processor = lambda l: l.lower()  # 如果需要忽略大小写，转换为小写
    else:
        line_processor = lambda l: l          # 否则保持原样

    for line in f:                            # 遍历文件的每一行
        child.send(line_processor(line))      # 处理行并发送给子协程

"""
3. grep协程 - 模式匹配器
"""
@coroutine  # 使用装饰器自动预激
def grep(substring, case_insensitive, child):
    if case_insensitive:
        substring = substring.lower()         # 将搜索模式转为小写
    while True:                               # 无限循环，等待数据
        text = (yield)                        # 1. 接收数据（从cat发送来的行）
        child.send(text.count(substring))     # 2. 计算模式出现次数，发送给count协程

"""
4. count协程 - 计数器
"""
@coroutine  # 使用装饰器自动预激
def counter(substring):
    n = 0                                    # 初始化计数器
    try:
        while True:                           # 无限循环，等待数据
            n += (yield)                      # 1. 接收数字并累加（从grep发送来的计数）
    except GeneratorExit:                     # 2. 协程结束时执行
        print(substring, n)                   # 打印最终结果

if __name__ == '__main__':
    import argparse                           # 导入命令行参数解析模块

    parser = argparse.ArgumentParser()        # 创建解析器
    parser.add_argument('-i', action='store_true',dest='case_insensitive')  # -i 选项：是否忽略大小写
    parser.add_argument('pattern', type=str)  # 必需参数：搜索模式
    parser.add_argument('infile', type=argparse.FileType('r'))  # 必需参数：输入文件

    args = parser.parse_args()               # 解析命令行参数

    # 构建协程管道：cat → grep → count
    cat(args.infile,
        args.case_insensitive,
        grep(args.pattern,
             args.case_insensitive,
             counter(args.pattern)))


"""
数据流示例
假设运行：python script.py -i "hello" input.txt

管道构建（从内向外）：

text
count("hello") → grep("hello", True, count) → cat(file, True, grep)
执行过程：

text
cat读取文件 → 发送每行给grep → grep统计"hello"出现次数 → 发送计数给count → count累加计数
结束时：

cat读取完所有行后结束

grep和count协程一直运行（while True循环）

程序结束时，count协程触发GeneratorExit异常，打印最终结果

关键点
协程管道：数据从cat流向grep，再流向count

生成器/协程：使用yield接收数据，send()发送数据

装饰器模式：@coroutine自动预激协程

惰性计算：数据流式处理，不需要一次性加载所有数据到内存

==============================================================

整个程序的工作流程：

从命令行读取参数，包括是否忽略大小写、要查找的模式（子字符串）和输入文件。

创建count协程，它等待接收数字并累加，当协程关闭时打印结果。

创建grep协程，它接收count协程作为子协程。grep协程等待接收文本，计算子字符串在文本中出现的次数，然后将次数发送给count协程。

调用cat函数，它读取文件的每一行，根据是否忽略大小写进行处理，然后发送给grep协程。

注意：在管道中，数据流向是：cat读取文件并发送行给grep，grep计算每行中子字符串出现的次数并发送给count，count累计次数。

当文件读取完毕，cat函数执行完毕，然后grep协程和count协程会因为没有更多的数据而关闭。count协程在关闭时（GeneratorExit异常）打印结果。

但是，注意代码中并没有显式关闭grep和count协程。实际上，当cat函数结束后，grep协程会一直等待，而count协程也会一直等待。不过，由于grep和count是无限循环，所以它们会一直等待，直到程序结束。在程序结束时，这些协程会被垃圾回收，从而触发GeneratorExit异常。

但是，更优雅的做法是显式关闭协程。这里没有关闭是因为cat函数不是协程，而是一个普通函数，它执行完就结束了。而grep和count是协程，它们会在yield处挂起。实际上，当cat函数执行完，程序就结束了，所以协程也会被销毁。

不过，在更复杂的程序中，我们可能需要显式关闭协程。但在此例中，由于程序简单，所以没有问题。
"""
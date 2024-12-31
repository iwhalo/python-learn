# 注意：爬取的数据以字典的形式放入了self.data属性中[{},{},{}]
# 如需直接使用需要把数据类型转换为列表，把self.data换成自己的数据存储变量名
import csv

# 获取header为第一行的字段名
header=self.data[0].keys()
# 写入文件test.csv
with open('test.csv','w',encoding='utf-8') as f:
    # 提前预览列名，当下面代码写入数据时，会将其一一对应
    witer=csv.DictWriter(f,fieldnames=header)
    # 写入列名
    witer.writeheader()
    # 写入字典中的数据
    witer.writerows(self.data)
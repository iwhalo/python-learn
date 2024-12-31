"""
爬取的数据以字典的形式放入了self.data属性中需要应用xlwt的包
"""

import xlwt




# 实例化一个xlwt对象
workbook=xlwt.Workbook(encoding='utf-8')

# 新建一个Excel书签，名为test
sheet1=workbook.add_sheet('test')

# 获取字段
header=list(self.data[0].keys())

# 使用for循环，字段数的长度和字段
for i,key in zip(range(len(header)),header):
    # excel写入字段名
    sheet1.write(0,i,key)

# 使用两个for循环，j用来控制写入数据的Excel的行数，m用来控制列数，而key则是用来取字典的数据
for j in range(1,len(self.data)+1):
    for m,key in zip(range(len(header)),header):
        # 写入数据
    sheet1.write(j,m,self.data[j-1][key])

# 保存文件路径，不用新建Excel文件，自动生成

workbook.save(r'零基础学爬虫/7【零基础学爬虫】数据存储几种方式-猿榜编程-微信公众号-2025-09-17/code/test.xlsx')
"""
爬取的数据还是存放在类的self.data属性中
mongodb数据库没有表的概念，数据的写入相对较为简单一点
"""

# 连接MongoDB
mdb=MongoClient('localhost',27017)

# 指定MongoDB的库的集合名称，不用新建，运行后直接创建
db=mdb.test['movie_info']

#for循环（self.data的数据类型为列表，中间的数据格式为字典[{},{}]）拿取数据字典格式
for i in self.data:
    # 判断数据是否为字典类型，如果是，写入
    if isinstance(i,dict):
        db.insert_one(i)
    #     如果不是的，则报i的title字段+写入数据失败
    else:
        print(i['title'],'写入失败')
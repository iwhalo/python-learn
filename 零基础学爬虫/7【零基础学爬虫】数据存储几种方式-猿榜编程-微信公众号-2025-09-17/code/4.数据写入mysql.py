"""爬取的数据还是存放在类的self.data属性中"""
import pymysql

# 连接mysql数据库，注：注意指定database的名称
db=pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    db='test',
    charset='utf8'
)

# 实例化一个游标对象
cursor=db.cursor()

# 创建两个字段，keys为sql语句的字段的站位字段，values为数据的站位字符串
keys=','.join(self.data[0].keys())
values=','.join(['%s']*len(self.data[0]))

# 这里的mysql数据库的表需要提前创建好
# 利用上面的站位字符串，构造一个通用的sql语句
sql='insert into movie_list(id,{key}) values (null,{values})'.format(key=keys,values=values)

# for循环把数据取成字典类型
for i in self.data:
    # 先获取字典值的数据为value，每一个数据赋值给一个变量
    value=list(i.values())
    title=value[0][0]
    start=value[1][0]
    actor=value[2]
    # 写一个报错，增加容错率
    try:
        if cursor.execute(sql,(title,start,actor)):
            print(title,'success')
    except:
            db.rollback()

# 需要使用这个db.commit()，sql语句才会生效
db.commit()
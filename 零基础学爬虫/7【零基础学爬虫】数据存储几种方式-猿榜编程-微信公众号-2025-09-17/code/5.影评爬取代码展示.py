import csv
import xlwt
from elasticsearch import Elasticsearch
from base import Sqide
from lxml import etree
import pymysql
from pymongo import MongoClient

import requests


class Test(Sqide):
    url = r'https://ssr1.scrape.center/'
    url_list = []
    data = []

    def product(self):
        response = requests.get(self.url)
        content = response.content.decode('utf8')
        html = etree.HTML(content)
        urls = html.xpath('//div[@class="el-card item m-t is-hover-shadow"]//a[@class="name"]/@href')
        # 电影链接》》》 ['/detail/1', '/detail/2', '/detail/3', '/detail/4', '/detail/5', '/detail/6', '/detail/7', '/detail/8', '/detail/9', '/detail/10']
        print("获取当前url页面上面每个电影链接》》》", urls)
        for i in urls:
            self.url_list.append('https://ssr1.scrape.center' + str(i))
        print(self.url_list)
        """
        ['https://ssr1.scrape.center/detail/1', 'https://ssr1.scrape.center/detail/2', 'https://ssr1.scrape.center/detail/3', 'https://ssr1.scrape.center/detail/4', 'https://ssr1.scrape.center/detail/5', 'https://ssr1.scrape.center/detail/6', 'https://ssr1.scrape.center/detail/7', 'https://ssr1.scrape.center/detail/8', 'https://ssr1.scrape.center/detail/9', 'https://ssr1.scrape.center/detail/10']
        """

    def consumer(self):
        for i in self.url_list:
            response = requests.get(i)
            content = response.content.decode('utf8')
            # print("获取每个电影链接地址请求的返回内容content》》》",content)
            html = etree.HTML(content)
            # print("将每个电影链接地址请求的返回内容生成HTML树》》》",content)
            title = html.xpath('//h2[@class="m-b-sm"]/text()')
            star = html.xpath(
                '//div[@class="el-col el-col-24 el-col-xs-8 el-col-sm-4"]//p[@class="score m-t-md m-b-n-sm"]/text()')
            actors = html.xpath('//div[@class="el-card__body"]/p[@class="name text-center m-b-none m-t-xs"]/text()')[0]
            movie_dict = {
                'title': title,
                'star': star,
                'actor': actors
            }
            print("获取每部电影的电影名称、评分、演员表》》》",movie_dict)
            self.data.append(movie_dict)
        print("\n\n当前页面所有电影数据self.data》》》",self.data)

    def save_csv(self):
        header = self.data[0].keys()
        print("获取每部电影数据的keys》》》",header)  # dict_keys(['title', 'star', 'actor'])
        # 写入文件test.csv
        with open('test.csv', 'w', encoding='utf-8') as f:
            # 提前预览列名，当下面代码写入数据时，会将其一一对应
            writer = csv.DictWriter(f, fieldnames=header)
            # 写入列名
            writer.writeheader()
            # 写入字典中的数据
            writer.writerows(self.data)

    def save_excel(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet('test')
        header = list(self.data[0].keys())
        print("len(header)>>>",len(header)) # len(header)>>> 3
        print("range(len(header))>>>",range(len(header))) # range(len(header))>>> range(0, 3)
        print("zip(range(len(header)), header)>>>",zip(range(len(header)), header)) # zip(range(len(header)), header)>>> <zip object at 0x0000022542511A00>
        for i, key in zip(range(len(header)), header):
            sheet1.write(0, i, key)

        for j in range(1, len(self.data) + 1):
            for m, key in zip(range(len(header)), header):
                sheet1.write(j, m, self.data[j - 1][key])

        workbook.save(
            r'D:\PycharmProjects\python-learn\零基础学爬虫\7【零基础学爬虫】数据存储几种方式-猿榜编程-微信公众号-2025-09-17\code\test.xlsx')

    def save_mongo(self):
        mdb = MongoClient(
            host='localhost',
            port=27017
        )
        db = mdb.test['movie_info']
        for i in self.data:
            if isinstance(i, dict):
                db.insert_one(i)
            else:
                print(i['title'], '写入失败')

    def save_mysql(self):
        db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='test',
            charset='utf8'
        )
        cursor = db.cursor()
        keys = ','.join(self.data[0].keys())
        values = ','.join(['%s'] * len(self.data[0]))
        sql = 'insert into movie_list(id,{key}) values(null,{values})'.format(key=keys, values=values)

        for i in self.data:
            value = list(i.values())
            title = value[0][0]
            star = value[1][0]
            actor = value[2]
            try:
                if cursor.execute(sql, (title, star, actor)):
                    print(title, "success")
            except:
                db.rollback()

            db.commit()

    def practice_es(self):
        es = Elasticsearch('http://127.0.0.1:9200/')
        es.index(
            index='xxx',
            doc_type='he',
            id=1,
            body=self.data
        )


if __name__ == '__main__':
    Test().product()
    Test().consumer()
    # Test().save_csv()
    Test().save_excel()
    # Test().save_mysql()
    # Test().save_mongo()
    # Test().practice_es()

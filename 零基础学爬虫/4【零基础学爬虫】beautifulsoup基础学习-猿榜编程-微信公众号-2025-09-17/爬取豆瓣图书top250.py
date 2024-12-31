import random

import requests
from bs4 import BeautifulSoup

# User-Agent库，随机选取，防止被禁
USER_AGENT_LIST=[
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrom"
]

# 请求网页
def get_response(url):
    # random.choice从一个列表中随机选出请求头
    headers={
        'User-Agent':random.choice(USER_AGENT_LIST)
    }

    response=requests.get(url=url,headers=headers)
    response.raise_for_status()
    soup=BeautifulSoup(response.content,'lxml')

    return soup

# 找到每本书的链接
def get_book_url(page):
    if page>10:
        return []
    num=(page-1)*25
    url='https://book.douban.com/top250?start=%s'%str(num)
    print("\n当前页url：%s"%url)

    soup=get_response(url)
    book_div=soup.find('div',attrs={'class':'indent'})
    books=book_div.findAll('tr',attrs={'class':'item'})
    urls=[book.td.a['href'] for book in books]

    print("获取第 %s 页"%page,urls)

    return urls

# 获取每本书的信息
def get_book_info(book_url):
    soup=get_response(book_url)

    div_info=soup.find('div',attrs={'id':'info'})

    book_author = div_info.a.text.split(' ')[-1]         #将空格去除

    book=soup.find('div',attrs={'class':'rating_wrap clearbox'})

    book_name= soup.find('span',attrs={'property':'v:itemreviewed'}).text

    book_grade = book.find('strong',attrs={'class':'ll rating_num '}).text

    book_man = book.find('a',attrs={'class':'rating_people'}).span.text

    book_info={}

    book_info['name']=book_name
    book_info['author']=book_author
    book_info['rating_num']=int(book_man)
    book_info['grade']=book_grade
    print(book_info)


    return book_info

if __name__ == '__main__':
    all_urls=[]
    # 从第1页到第10页爬取，链接拼接到一起。
    for page in range(1,11):
        urls=get_book_url(page)
        all_urls=all_urls+urls

    print("获取到的链接数：",len(all_urls))

    out=''
    for url in all_urls:
        try:
            info=get_book_info(url)
        except Exception as e:
            print(e)
            continue
        out=out+str(info)+'\n'

    with open('douban_book_top250.txt','w') as f:
        f.write(out)
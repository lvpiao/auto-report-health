# encoding:utf-8
import requests
import math
import time
from bs4 import BeautifulSoup
from threading import Lock, Thread, Semaphore

search_url = "https://www.sinchew.com.my/app_if/searchWebArticles"

# 请求参数
data = {"columnId": 0,
        "siteID": 1,
        "count": 100,
        "start": 0,
        "key": ""}
fo = {}

lock = Lock()
threadCnt = Semaphore(8)
page_size = 20


def getArticlesByPage(cur_page: int):
    print("cur_page:"+str(cur_page))
    data["start"] = cur_page*page_size
    response = requests.get(search_url, params=data)
    json_data = response.json()
    articles_list = json_data["articles"]
    if len(articles_list) == 0:
        return
    for article in articles_list:
        # 读取需要数据
        item = []
        # 过滤2019-12-21 之前的新闻
        if article["publishtime"] < "2019-12-21":
            continue
        print("cur_page:"+str(cur_page) + article["textTitle"])
        item.append(article["url"])
        item.append(article["textTitle"].replace(',', "，"))
        item.append(article["publishtime"].split(" ")[0])
        item.append(article["textAbstract"])
        # 获取文章内容
        html = requests.get(article["url"]).text
        item.append(BeautifulSoup(html, "lxml").select(
            '#dirnum')[0].text.strip().replace(',', "，"))
        lock.acquire(timeout=5)
        fo.write(",".join(item)+"\n")
        lock.release()
    # 释放一个线程
    threadCnt.release()


def getArticles(keyword: str):
    data["key"] = keyword
    print(keyword)
    response = requests.get(search_url, params=data)
    json_data = response.json()
    if type(json_data) == int:
        return
    article_count = int(json_data["countResult"])
    data["count"] = article_count
    for cur_page in range(math.ceil(article_count/page_size)):
        threadCnt.acquire()
        Thread(target=getArticlesByPage, args=(cur_page,)).start()


if __name__ == "__main__":
    keyword = input("关键字>>")
    try:
        fo = open(keyword.replace(" ", "_")+".csv", "w", encoding='utf-8')
        fo.write("文章链接,标题,发布时间,摘要,内容\n")
        getArticles(keyword)
    except Exception as identifier:
        print(identifier)
    finally:
        if fo:
            fo.close()
        print("爬取完成！！！")
        time.sleep(1)

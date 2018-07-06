#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import time,json
import requests
from requests.exceptions import RequestException
from lxml import etree
from bs4 import BeautifulSoup
from pyquery import PyQuery


def getPage(url):
    '''爬取指定url地址的信息'''
    try:
        # 定义请求头信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }
        # 执行爬取
        res = requests.get(url,headers = headers)
        # 判断并返回结果
        if res.status_code == 200:
            return res.text
        else:
            return None
    except RequestException:
        return None

def parsePage(content):
    '''解析爬取网页中内容，并返回结果'''
    # print(content)
    '''
    # 使用Xpath
    # 初始化，返回根节点对象
    html = etree.HTML(content)
    # 解析网页中<tr class="item">···</tr>信息
    items = html.xpath("//tr[@class='item']")
    # 解析每本图书具体信息
    for item in items:
        yield {
            'title':item.xpath(".//div[@class='pl2']/a/@title")[0],
            'image':item.xpath(".//img[@width='90']/@src")[0],
            'actor':item.xpath(".//p[@class='pl']/text()")[0].split('/').pop(0),
            'publisher': item.xpath(".//p[@class='pl']/text()")[0].split('/').pop(-3),
            'price': item.xpath(".//p[@class='pl']/text()")[0].split('/').pop(),
            'score':item.xpath(".//span[@class='rating_nums']/text()")[0],
        }
    '''
    '''
    # 使用BeautifulSoup
    # 初始化，返回BeautifulSoup对象
    soup = BeautifulSoup(content,'lxml')
    # 解析网页中<tr class="item">···</tr>信息
    items = soup.find_all(name="tr", attrs={"class":"item"})
    # 解析每本图书具体信息
    for item in items:
        yield {
            'title':item.select("div.pl2 a")[0].attrs['title'],
            'image':item.find(name="img",attrs={"width":"90"}).attrs['src'],
            'actor':item.select("p.pl")[0].get_text().split('/').pop(0),
            'publisher':item.select("p.pl")[0].get_text().split('/').pop(-3),
            'price':item.select("p.pl")[0].get_text().split('/').pop(),
            'score':item.select("span.rating_nums")[0].string,
        }
    '''
    # 使用pyquery
    # 初始化，返回pyquery对象
    doc = PyQuery(content)
    # 解析网页中<tr class="item">···</tr>信息
    items = doc("tr.item")
    # 解析每本图书具体信息
    for item in items.items():
        yield {
            'title':item.find('div.pl2 a').attr('title'),
            'image':item.find("a.nbg img").attr('src'),
            'actor':item.find("p.pl").text().split('/').pop(0),
            'publisher':item.find("p.pl").text().split('/').pop(-3),
            'price':item.find("p.pl").text().split('/').pop(),
            'score':item.find("div.star span.rating_nums").text(),
        }

def writeFile(content):
    '''写入文件'''
    with open('./豆瓣图书top250.txt','a', encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(offset):
    '''主程序函数，负责调度执行爬取处理'''
    url = 'https://book.douban.com/top250?start=' + str(offset)
    html = getPage(url) # 执行爬取
    if html:
        for item in parsePage(html): # 执行解析并遍历
            print(item)
            writeFile(item)  # 执行写操作

# 判断当前执行是否为主程序，并遍历调度主函数来爬去信息
if __name__ == '__main__':
    # main(0)
    for i in range(10):
        main(offset=i*25)
        time.sleep(1)

#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests
from lxml import etree
import re
import pymysql


class get_url:
    def __init__(self):
        self.ua = {
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }
        self.session = requests.Session()
        self.blog_urls = []
        self.plates_id = []
        self.conn_mysql = pymysql.connect(host='127.0.0.1', user='root', password='root', db='hexun')

    """
    @ 获取首页中的博客url及所有板块id
    """
    def hp_url(self, url):
        # get请求首页信息
        response = self.session.get(url, headers=self.ua, verify=False)
        homepage_data1 = response.content.decode('gbk')
        homepage_data2 = etree.HTML(homepage_data1)
        # 获取首页中的博客url
        homepage_urls = homepage_data2.xpath("//li/a/@href")
        for i in homepage_urls:
            if '_d.html' in i:
                self.blog_urls.append(i)
        # 获取所有板块的url
        plate = homepage_data2.xpath('//dd/a/@href')
        for j in plate:
            pat = 'http://blog.hexun.com/class(.*?).htm'
            try:
                id = re.compile(pat).findall(j)[0]
                self.plates_id.append(id)
            except Exception as Error:
                print(Error)
                continue

    """
    @ 获取板块中的博客url
    """
    def plate(self, plate_link):
        # get请求板块信息
        plate_response = self.session.get(plate_link, headers=self.ua, verify=False)
        plate_data1 = plate_response.content.decode('gbk')
        plate_data2 = etree.HTML(plate_data1)
        # 获取板块中博客url
        plate_blog_url = plate_data2.xpath('//dd[@class="txt"]/h2/a/@href')
        for k in plate_blog_url:
            if '_d.html' in k:
                self.blog_urls.append(k)

    """
    @ 获取博客信息
    """
    def get_blog(self, blog_url):
        headers = {
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'Referer': blog_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }
        try:
            # get请求博客信息
            blog_response = self.session.get(blog_url, headers=headers, verify=False)
            blog_data = blog_response.content.decode('gbk')
            tree_blog_data = etree.HTML(blog_data)
            # 获取博客title
            title = tree_blog_data.xpath('/html/head/title/text()')[0]
            # 获取博客的id
            pat = 'showArticleComments(.*?);'
            result = re.compile(pat, re.S).findall(blog_data)[0]
            article_id = eval(result)[1]
            blog_id = eval(result)[2]
            # 构造获取博客点击量和评论量的url
            url = 'http://click.tool.hexun.com/click.aspx?articleid=%s&blogid=%s' % (article_id, blog_id)
            # 获取博客的点击量和评论量
            response = self.session.get(url, headers=headers, verify=False)
            nums = re.compile(r'([0-9]\d*)').findall(response.text)
            click_count = nums[0]
            comment_count = nums[1]
            print('文章名：%s\n文章链接%s\n文章点击量%s\n文章评论数%s' % (title, blog_url, click_count, comment_count))
            print('-' * 100)
            # 写入数据库
            self.write_db(title, blog_url, click_count, comment_count)
        except Exception as err:
            print('-' * 100)
            print(err)

    """
    @ 写入数据库
    """
    def write_db(self, title, url, click_count, comment_count):
        sql = "insert into blog_info(title,url,clickCount,commentCount) values('" + title + "','" + url + "','" + click_count + "','" + comment_count + "')"
        self.conn_mysql.query(sql)
        self.conn_mysql.commit()


if __name__ == '__main__':
    url = 'http://blog.hexun.com/'
    a = get_url()
    # 请求首页信息
    a.hp_url(url)
    for i in a.plates_id:
        print('板块ID：%s' % i)
        # 每个板块请求5页的内容
        for x in range(0, 5):
            try:
                print('\t板块【%s】第%d页' % (i, x + 1))
                plate_link = 'http://blog.hexun.com/group/class%s_latest_p_%d.html' % (i, x + 1)
                a.plate(plate_link)
            except Exception as error:
                print(error)
                continue
    # 获取博客信息，并写入数据库
    for j in range(0, len(a.blog_urls)):
        blog_url = a.blog_urls[j]
        a.get_blog(blog_url)

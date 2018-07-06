import requests
from pyquery import PyQuery as pq
import redis


def main():
    # 使用requests爬取所有标签信息
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    res = requests.get(url)
    print('status: %d' % res.status_code)
    html = res.content.decode('utf-8')

    # 使用pyquery解析html文档
    doc = pq(html)
    # 获取网页中所有tag信息
    items = doc('table.tagCol tr td a')

    # 连接redis数据库
    conn_redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    # 遍历封装数据并返回
    for i in items.items():
        # 拼装tag的url
        tag = i.attr.href
        # 将信息以book:start_urls写入redis中
        conn_redis.lpush('book:tag_urls',tag)

    print('共计写入%d个tag信息' % (len(items)))

# 主程序
if __name__ == '__main__':
    main()
import requests
import re
import pymysql
from urllib.parse import quote


class taobao():
    def __init__(self):
        self.session = requests.Session()
        self.ua = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
        self.conn_mysql = pymysql.connect(host="127.0.0.1", user='root', password='root', db='tb')

    def get_info(self, page_url, urls, titles, prices, sales):
        response = self.session.get(page_url, headers=self.ua, verify=False)
        data = response.content.decode('utf-8')
        url_pat = '"p4pTags":.*?"detail_url":"(//.*?)"'
        all_url = re.compile(url_pat, re.S).findall(data)
        for i in all_url:
            a = i.encode('utf-8').decode('unicode_escape')
            b = 'https:' + a
            urls.append(b)
        title_pat = '"p4pTags":.*?"raw_title":"(.*?)"'
        all_title = re.compile(title_pat, re.S).findall(data)
        for j in all_title:
            titles.append(j)
        price_pat = '"p4pTags":.*?"view_price":"(.*?)"'
        all_price = re.compile(price_pat, re.S).findall(data)
        for k in all_price:
            prices.append(k)
        sale_pat = '"p4pTags":.*?"view_sales":"(.*?)"'
        all_sale = re.compile(sale_pat, re.S).findall(data)
        for l in all_sale:
            d = re.compile('([0-9]\d*)').findall(l)[0]
            sales.append(d)

    def insert_mysql(self, title, url, price, sale):
        sql = "insert into goods(title,url,price,sale) values('" + title + "','" + url + "','" + price + "','" + sale + "')"
        print(sql)
        self.conn_mysql.query(sql)
        self.conn_mysql.commit()


if __name__ == '__main__':
    name = quote('零食')
    a = taobao()
    for i in range(0, 100):
        page_url = 'https://s.taobao.com/search?q=%s&s=%d' % (name, i * 44)
        urls = []
        titles = []
        prices = []
        sales = []
        a.get_info(page_url, urls, titles, prices, sales)
        for k in range(0, len(urls)):
            title = titles[k]
            url = urls[k]
            price = prices[k]
            sale = sales[k]
            a.insert_mysql(title, url, price, sale)

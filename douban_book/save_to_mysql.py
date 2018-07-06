# 将redis中的item信息遍历写入数据库中
import json,redis,pymysql

def main():
    # 连接redis数据库
    conn_redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    # 连接mysql数据库
    conn_mysql = pymysql.connect(host='localhost',user='root',password='root',db='mydb',charset='utf8')
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn_mysql.cursor()


    while True:
        # FIFO(先入先出)模式为blpop,LIFO(后进先出)模式为brpop，获取键值
        source, data = conn_redis.blpop(["slave_book:items"])
        print(source)
        try:
            item = json.loads(data)
            # 拼装sql语句
            dd = dict(item)
            keys = ','.join(dd.keys())
            values = ','.join(['%s']*len(dd))
            sql = 'insert into books(%s) values(%s)' % (keys, values)
            # 指定参数，并执行sql添加
            cursor.execute(sql,tuple(dd.values()))
            # 事物提交
            conn_mysql.commit()
            print('写入信息成功：',dd['id'])
        except Exception as err:
            # 事务回滚
            conn_mysql.rollback()
            print('SQL执行错误，原因：',err)

# 主程序入口
if __name__ == '__main__':
    main()
import requests
import re
import xlwt
import time

# 存储信息列表
let_info = []

# 循环爬取70页
for i in range(0,70):
    print('获取第%d页信息' % (i+1))
    # 构造url
    url = 'http://sh.58.com/chuzu/pn'+str(i+1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    try:
        # 执行请求获取响应信息
        res = requests.get(url, headers=headers)
        # 从响应对象中读取信息并解码
        html = res.content.decode('utf-8')
        # 构造正则表达式
        pat = '''<div class="des">.*?<a href="(.*?)".*?target="_blank".*?>(.*?)\|(.*?)</a>.*?<p class="room">(.*?)&nbsp;&nbsp;&nbsp;&nbsp;(.*?)㎡</p>.*?biaoti_shangquan.*?>(.*?)</a>.*?<div class="money">.*?<b>(.*?)</b>'''
        # 使用正则解析信息
        dlist = re.findall(pat,html,re.S)
        print('第%d页有%d条租房信息' % (i+1, len(dlist)))
        if len(dlist) == 0:
            print('访问过于频繁，请使用浏览器打开网址：http://sh.58.com/chuzu/pn1/ 进行校验后重新爬取')
            break
        # 将信息逐条添加到信息列表
        for v in dlist:
            let_info.append(v)
    except Exception as e:
        print(e)
    # 设置间隔时间，防止ip被封
    time.sleep(2)

# for i in range(0,len(let_info)):
#     data = let_info[i][0]+'\t'+let_info[i][1].replace('\n','').replace(' ','')+'\t'+let_info[i][2].replace(' ','')+'\t'+let_info[i][3].replace(' ','')+'\t'+let_info[i][4]+'\t'+let_info[i][5]+'\t'+let_info[i][6]+'\n'
#     print(data)

# 构造excel表格头
new_excel = xlwt.Workbook()
new_sheet = new_excel.add_sheet('sheet')
new_sheet.write(0,0,'出租方式')
new_sheet.write(0,1,'简介')
new_sheet.write(0,2,'房间')
new_sheet.write(0,3,'面积(㎡)')
new_sheet.write(0,4,'商圈')
new_sheet.write(0,5,'价格(元)')
new_sheet.write(0,6,'详情链接')

# 将信息写入表格
print("共获取到%d条信息\n将数据写入表格中···" % len(let_info))
for i in range(0,len(let_info)):
    new_sheet.write(i+1,0,let_info[i][1].replace('\n','').replace(' ',''))  # 出租方式
    new_sheet.write(i+1,1,let_info[i][2].replace(' ',''))   # 简介
    new_sheet.write(i+1,2,let_info[i][3].replace(' ',''))   # 房间
    # 不能转为float类型的保持原样
    try:
        new_sheet.write(i+1,3,float(let_info[i][4]))    # 面积
    except:
        new_sheet.write(i+1,3,let_info[i][4])
    new_sheet.write(i+1,4,let_info[i][5])   # 商圈
    # 不能转为float类型的保持原样
    try:
        new_sheet.write(i+1,5,float(let_info[i][6]))    # 价格
    except:
        new_sheet.write(i+1,5,let_info[i][6])
    new_sheet.write(i+1,6,let_info[i][0])   # 链接
new_excel.save(r'58上海租房信息request.xls')
print("写入完成！")
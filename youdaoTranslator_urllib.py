from urllib import request,parse
import json
import hashlib
import time
import random

def translate(keyword):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
   
    '''
    请求参数中的salt和sign是通过js代码按照一定规则生成的，打开源代码找到fanyi.min.js文件后将其格式化
    搜索'translate ='可得出其参数的生成规则，用python代码将其实现；
    '''
    S = 'fanyideskweb'
    n = keyword
    r = str(int(time.time()*1000) + random.randint(0,10))
    D = "ebSeFb%=XZ%T[KZ)c(sy!"
    o = hashlib.md5((S + n + r + D).encode('utf-8')).hexdigest()
    
    # 定义请求参数，并编码转换；
    data = {
        'i': keyword,
        'from':'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': r,
        'sign': o,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTIME',
        'typoResult': 'false',
    }
    data = parse.urlencode(data)

    # 设置hearders头信息
    headers = {
        'Content-Length': len(data),
        'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=72672313.57166907; _ga=GA1.2.1559468220.1528697398; _gid=GA1.2.1174540348.1528697398; OUTFOX_SEARCH_USER_ID=2116617538@10.169.0.84; JSESSIONID=aaaufXUk0YpjI57WIuZpw; ___rl__test__cookies=1528795745328',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
    }
    try:
        # 发送请求，爬取信息
        req = request.Request(url,data = bytes(data,encoding='utf-8'),headers=headers)
        res = request.urlopen(req)
        # print(res.read().decode('utf-8'))

        # 解析结果
        str_json = res.read().decode('utf-8')
        # print(str_json)
        # 结果长度
        length = len(json.loads(str_json))
        # 状态码
        errorCode = json.loads(str_json)['errorCode']
        # 若状态码为0，则有翻译结果
        if errorCode == 0:
            # 筛选出翻译结果
            # 判断结果长度，若长度为3，则只有普通翻译结果，否则有详细结果
            if length == 3:
                # 普通结果
                result = json.loads(str_json)['translateResult'][0][0]['tgt']
                print(result)
            else:
                # 详细结果
                result = json.loads(str_json)['smartResult']['entries'][1:]
                for i in result:
                    print(i.replace('\r\n',''))
        else:
            print('请重新输入')
    except Exception as e:
        if hasattr(e,"code"):
            print("HTTPError")
            print(e.reason)
            print(e.code) 
        elif hasattr(e,"reason"):
            print('URLError')
            print(e.reason)
        else:
            print(e)

if __name__ == '__main__':
    while True:
        keyword = input("请输入需要翻译的词语(按q退出): ")
        if keyword == 'q':
            break
        translate(keyword)
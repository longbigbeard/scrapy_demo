#encoding=utf-8
from urllib import request,parse
import time,random
'''
i = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10)),
i = n.md5("fanyideskweb" + t + r + "ebSeFb%=XZ%T[KZ)c(sy!");
'''


def getSalt():
    salt = int(time.time()*1000) + random.randint(0,10)
    return salt


def getMd5(v):
    import hashlib
    md5 = hashlib.md5()
    md5.update(v.encode('utf-8'))
    sign = md5.hexdigest()
    return sign


def getsign(key,salt):
    sign = "fanyideskweb" + key + str(salt) + "ebSeFb%=XZ%T[KZ)c(sy!"
    sign = getMd5(sign)
    return sign


def youdao(key):
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    salt = getSalt()
    data = {
        "i": key,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": str(salt),
        "sign": getsign(key,salt),
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION",
        "typoResult": "false"
    }
    data = parse.urlencode(data).encode()

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        # "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": len(data),
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Cookie": "OUTFOX_SEARCH_USER_ID=1144300821@10.168.8.63;JSESSIONID=aaaHApF5PZ25B-fIUd9pw;OUTFOX_SEARCH_USER_ID_NCOO=1594679395.7539725;fanyi-ad-id=44881;fanyi-ad-closed=1;__rl__test__cookies=1528959059311",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36X-Re",
        "quested-With": "XMLHttpRequest",
    }
    req = request.Request(url=url,data=data,headers=headers)
    rsp = request.urlopen(req)
    html = rsp.read()
    print(html)
if __name__ == '__main__':
    youdao("boy")
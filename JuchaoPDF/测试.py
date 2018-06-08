import requests
import time

URL = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


START_DATE = '2001-09-20'  # 首家农业上市企业的日期
END_DATE = str(time.strftime('%Y-%m-%d'))  # 默认当前提取，可设定为固定值
# OUT_DIR = 'D:/workspace/cninfo/report/agriculture'
# OUT_DIR = '/home/captain/PycharmProjects/reportPDF'
OUTPUT_FILENAME = '年度审计报告'
# 板块类型：shmb（沪市主板）、szmb（深市主板）、szzx（中小板）、szcy（创业板）
PLATE = 'szzx;'


MAX_PAGESIZE = 49
MAX_RELOAD_TIMES = 5
RESPONSE_TIMEOUT = 10





def get_response(page_num, return_total_count=False):

    query = {
        'stock':'',
        'searchkey': '年度审计报告',
        'plate':'',
        'category':'',
        'trade':'',
        'column': 'szse',
        'columnTitle': '历史公告查询',
        'pageNum': page_num,
        'pageSize': MAX_PAGESIZE,
        'tabName': 'fulltext',
        'sortName':'',
        'sortType':'',
        'limit':'',
        'showTitle':'',
        'seDate': START_DATE + '~' + END_DATE,
    }

    res = requests.post(URL, query, HEADER, timeout=RESPONSE_TIMEOUT)
    print(res.text)


get_response(1,True)
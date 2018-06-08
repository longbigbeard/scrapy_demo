
# encoding: utf-8

import csv
import math
import os
import random
import time
import requests

"""
*****************
可改配置，酌情更改
*****************
"""
START_DATE = '2001-09-20'  # 首家农业上市企业的日期
END_DATE = str(time.strftime('%Y-%m-%d'))  # 默认当前提取，可设定为固定值
OUT_DIR = '/home/captain/PycharmProjects/reportPDF'
OUTPUT_FILENAME = '年度审计报告'
# 板块类型：shmb（沪市主板）、szmb（深市主板）、szzx（中小板）、szcy（创业板）
PLATE = 'szzx;'
# 公告类型：category_scgkfx_szsh（首次公开发行及上市）、category_ndbg_szsh（年度报告）、category_bndbg_szsh（半年度报告）
#CATEGORY = 'category_ndbg_szsh;'
"""
*****************
固定配置，勿改
*****************
"""
URL = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
MAX_PAGESIZE = 50
MAX_RELOAD_TIMES = 5
RESPONSE_TIMEOUT = 10



def standardize_dir(dir_str):
    #先判断这个文件夹是否存在，不存在报错
    assert (os.path.exists(dir_str)), 'Such directory \"' + str(dir_str) + '\" does not exists!'
    if dir_str[len(dir_str) - 1] != '/':
        return dir_str + '/'
    else:
        return dir_str
"""
这有一个问题，目录是提前设置好的，可以调用函数，来提取当前目录，保存到程序存在的目录
"""




# 参数：页面id(每页条目个数由MAX_PAGESIZE控制)，是否返回总条目数(bool)
def get_response(page_num, return_total_count=False):
    query = {
        'stock': '',
        'searchkey': '年度审计报告',
        'plate': '',
        'category': '',
        'trade': '',
        'column': 'szse',
        'columnTitle': '历史公告查询',
        'pageNum': page_num,
        'pageSize': MAX_PAGESIZE,
        'tabName': 'fulltext',
        'sortName': '',
        'sortType': '',
        'limit': '',
        'showTitle': '',
        'seDate': START_DATE + '~' + END_DATE,
    }

    result_list = []
    reloading = 0
    while True:
        reloading += 1
        if reloading > MAX_RELOAD_TIMES:
            return []
        elif reloading > 1:
            __sleeping(random.randint(5, 10))  #随机睡眠5~10秒
            print('... reloading: the ' + str(reloading) + ' round ...')

        try:
            res = requests.post(URL, query, HEADER, timeout=RESPONSE_TIMEOUT)
        except Exception as e:
            print(e)
            continue
        if res.text == '':
            print("-----------空-------------")
        if res.status_code == requests.codes.ok and res.text != '':  #取值之后跳出，否则循环在请求一次
            break
    my_query = res.json()#转化为json？

    try:
        res.close()
    except Exception as e:
        print(e)
    if return_total_count:
        return my_query['totalRecordNum']
    else:
        for each in my_query['announcements']:  # 链接所在的位置“announcements”
            # 做拼接，我记得有个方法是用来做拼接的----------------------------------------------------------------///标记
            file_link = 'http://www.cninfo.com.cn/' + str(each['adjunctUrl'])  # “adjunctUrl”链接位置
            file_name = __filter_illegal_filename(
                str(each['secCode']) + str(each['secName']) + str(each['announcementTitle']) +
                file_link[-file_link[::-1].find('.') - 1:]  # 最后一项是获取文件类型后缀名
            )
            result_list.append([file_name, file_link])
        return result_list  # 返回了一个列表，记录了当前页内链接的名字和下载地址


def __log_error(err_msg):
    err_msg = str(err_msg)
    print(err_msg)
    with open(error_log, 'a', encoding='gb18030') as err_writer:
        err_writer.write(err_msg + '\n')


def __sleeping(sec):
    if type(sec) == int:
        print('... sleeping ' + str(sec) + ' secong ...')
        time.sleep(sec)


def __filter_illegal_filename(filename):
    illegal_char = {
        ' ': '',
        '*': '',
        '/': '-',
        '\\': '-',
        ':': '-',
        '?': '-',
        '"': '',
        '<': '',
        '>': '',
        '|': '',
        '－': '-',
        '—': '-',
        '（': '(',
        '）': ')',
        'Ａ': 'A',
        'Ｂ': 'B',
        'Ｈ': 'H',
        '，': ',',
        '。': '.',
        '：': '-',
        '！': '_',
        '？': '-',
        '“': '"',
        '”': '"',
        '‘': '',
        '’': ''
    }
    for item in illegal_char.items():
        filename = filename.replace(item[0], item[1])
    return filename


if __name__ == '__main__':
    # 初始化重要变量
    out_dir = standardize_dir(OUT_DIR) #保存路径
    error_log = out_dir + 'error.log'
    output_csv_file = out_dir + OUTPUT_FILENAME.replace('/', '') + '_' + \
                      START_DATE.replace('-', '') + '-' + END_DATE.replace('-', '') + '.csv'
    # 获取记录数、页数
    item_count = get_response(1, True)
    assert (item_count != []), 'Please restart this script!'#如果无记录则退出
    begin_pg = 1
    end_pg = int(math.ceil(item_count / MAX_PAGESIZE))#math.ceil(x)返回大于等于参数x的最小整数,即对浮点数向上取整
    print('Page count: ' + str(end_pg) + '; item count: ' + str(item_count) + '.')
    time.sleep(2)#sleep() 方法暂停给定秒数后执行程序

    # 逐页抓取
    with open(output_csv_file, 'w', newline='', encoding='gb18030') as csv_out:
        writer = csv.writer(csv_out)
        for i in range(begin_pg, end_pg + 1):
            row = get_response(i)
            if not row:
                __log_error('Failed to fetch page #' + str(i) +
                            ': exceeding max reloading times (' + str(MAX_RELOAD_TIMES) + ').')
                continue
            else:
                writer.writerows(row)
                last_item = i * MAX_PAGESIZE if i < end_pg else item_count
                print('Page ' + str(i) + '/' + str(end_pg) + ' fetched, it contains items: (' +
                      str(1 + (i - 1) * MAX_PAGESIZE) + '-' + str(last_item) + ')/' + str(item_count) + '.')

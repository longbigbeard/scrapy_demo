# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import csv
import time

OUT_DIR = '/home/captain/PycharmProjects/reportPDF'
base_url = 'http://blog.jobbole.com/all-posts/page/'

session = requests.session()
inum=0

def zhuqu(page):
    url_list = []
    url = base_url+str(page)+"/"
    # print(url)
    res = session.get(url=url)
    soup = BeautifulSoup(res.text, 'html.parser')
    post_nodes = soup.select("#archive .floated-thumb .post-thumb a")
    for post_node in post_nodes:
        post_url = post_node.get("href")
        url_list.append([post_url])
        # i+=1
        # print(i,post_url)
    # print(url_list)
    return url_list

with open("伯乐文章", 'w', newline="", encoding='utf-8') as csv_out:
        writer = csv.writer(csv_out)
        for i in range(559):
            if i%10==0:
                time.sleep(1)
            row =zhuqu(i)
            if not row:
                print("有错误")
                continue
            else:
                writer.writerows(row)
                print(inum,"成功")
                inum+=1
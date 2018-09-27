#encoding = utf-8

import csv
import time
OUT_DIR = '/home/captain/PycharmProjects/reportPDF'


with open("伯乐文章", 'r', newline="", encoding='gb18030') as csv_out:
    row = csv.reader(csv_out)
    for rows in row:
        print(rows)
        # time.sleep(10)


'''
豆瓣电影排行版
'''
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

dirver = webdriver.Chrome()

url = "http://www.baidu.com"

dirver.get(url)
text = dirver.find_element_by_id('wrapper').text
print(text)
print(dirver.title)
dirver.find_element_by_id('kw').send_keys(u"大熊猫")
dirver.find_element_by_id('su').click()
time.sleep(5)
dirver.save_screenshot('1.png')
# 获取cookie
print(dirver.get_cookies())

dirver.find_element_by_id('kw').send_keys(Keys.CONTROL,'a')
dirver.find_element_by_id('kw').send_keys(Keys.CONTROL,'x')

dirver.find_element_by_id('kw').send_keys(u'空间')
dirver.save_screenshot('2.png')

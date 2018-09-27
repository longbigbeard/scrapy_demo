# -*- coding: utf-8 -*-
import scrapy
from WSYU.items import WsyuItem
import datetime
from urllib import parse
from scrapy.http import Request

class WsyuSpider(scrapy.Spider):
    name = 'wsyu'
    allowed_domains = ['wsyu.edu.cn']
    # start_urls = ['http://www.wsyu.edu.cn/',]
    start_urls = ['http://www.wsyu.edu.cn/',]
    html_url_set = []
    other_url_set =[]
    wenjian_end = ["@", ".pdf", ".jpg", ".gif", ".png", ".doc", ".xls", ".ppt", ".mp3", ".rar", ".zip",]


    def do_fiter(self,all_urls):
        for one_url in all_urls:
            if any(u in one_url for u in self.wenjian_end):
                self.other_url_set.append(one_url)
            else:
                pass
        return all_urls



    def parse(self, response):
        # 获取所有的地址链接
        all_urls = response.xpath('//a/@href').extract()
        all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        all_urls1 = self.do_fiter(all_urls)
        # all_urls2 = list(filter(lambda x:True if x.startswith('\'http') else False, all_urls1))
        if all_urls1!=None:
            for one_url in all_urls1:
                if one_url not in self.html_url_set and one_url not in self.other_url_set:
                    self.html_url_set.append(one_url)
                    # yield self.make_requests_from_url(one_url)
                    yield Request(parse.urljoin(response.url,one_url),callback=self.download_parse)
                    # 回调函数默认为parse


        else:
            yield Request(url=self.html_url_set[-2],callback=self.parse)
        # yield Request(self.url_set[-1],callback=self.parse)


    def download_parse(self,response):
        # if ".pdf" in response.url:
        #     pass
        # elif ".jpg" or ".gif" or ".png" in response.url:
        #     pass
        # elif response.url.endswith(".doc"):
        #     pass
        # # elif ".xls" or ".xlsx" in one_url:
        # # 因为 出现".xlsx"必定包含".xls"，所以 暂时不采用上述写法
        # elif ".xls" in response.url:
        #     pass
        # elif ".ppt" in response.url:
        #     pass
        # elif ".mp3" in response.url:
        #     pass
        # elif ".rar" or ".zip" in response.url:
        #     pass
        #
        # else:

        item = WsyuItem()
        item['url'] = response.url
        # print(item['url'])
        item['content'] = response.text
        # print(item['content'])
        item['create_time'] = datetime.datetime.now()
        # print(item['create_time'])
        yield item
        # yield Request(url=response.url ,callback=self.parse)
        yield self.make_requests_from_url(response.url)

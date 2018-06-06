# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/']

    def parse(self, response):
        title = response.xpath("//div[@class='entry-header']/h1/text()")
        crate_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first("").strip().replace("·","").strip()
        praise_nums =  response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first("")
        fav_nums = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract_first("")
        match_re = re.match(".*(\d+).*",fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first("")
        match_re = re.match(".*(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        content = response.xpath('//div[@class="entry"]').extract_first("")
        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        title = response.css(".entry-header h1::text").extract()
        crate_date = crate_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first("").strip().replace("·","").strip()
        praise_nums = response.css(".vote-post-up h10::text").extract_first("")
        fav_nums = response.css(".bookmark-btn::text").extract_first("")
        match_re = re.match(".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        comment_nums = response.css("a[href='#article-comment'] span::text").extract_first("")
        match_re = re.match(".*(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        content = response.css("div.entry").extract_first("")
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        pass


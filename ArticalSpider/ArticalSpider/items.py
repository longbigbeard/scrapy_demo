# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import Join


class ArticalspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



# 加后缀
def add_jobbole(value):
    return value+"-jobbole"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value,"%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


#提取评论等中的数字值
def get_nums(value):
    match_re = re.match(".*(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums



class ArticleItemLoader(ItemLoader):
    #自定义itemloder
     default_output_processor = TakeFirst()


def remove_comment_tags(value):
    #去掉tags中的评论
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value

class JobboleArticalItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(add_jobbole)
    )
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        utput_processor=MapCompose(return_value)
    )
    # front_image_path =scrapy.Field()
    praise_nums =scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor = MapCompose(remove_comment_tags),
        output_processor = Join(",")
    )
    content = scrapy.Field()


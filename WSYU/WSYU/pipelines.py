# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class WsyuPipeline(object):
    def process_item(self, item, spider):
        return item


# 异步写入
class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):

        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)#可变化的方式××
        return cls(dbpool)

    def process_item(self,item,spider):
        #使用twisted将MySQL插入变成异步

        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)#处理异常

    def handle_error(self,failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                     insert into info_all(url,content,create_time)
                     values (%s,%s,%s)
                   """
        cursor.execute(insert_sql, (
        item["url"], item["content"], item["create_time"] ))


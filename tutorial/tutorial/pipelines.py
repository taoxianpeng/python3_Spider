# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class TutorialPipeline(object):
    def __init__(self):
        self.connect=sqlite3.connect('doubanfilm.db')
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        try:
            sql_insert="insert into user (name,score,people_num,country,time) values (?,?,?,?,?)"
            
            
            self.cursor.execute(sql_insert,(item['name'],item['score'], item['people_num'],item['country'],item['time']))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            print(e)

        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
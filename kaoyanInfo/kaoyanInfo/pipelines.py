# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class KaoyaninfoPipeline(object):
    def __init__(self):
        self.connect=sqlite3.connect('kaoyaninfo.db')
        self.cursor = self.connect.cursor()
        self.add_num=0
        
    def process_item(self, item, spider):
        try:
            sql_isExist="select * from user where url = ?"
            sql_insert="insert into user (school,subjects,years,pnum,time,url) values (?,?,?,?,?,?)"
            
            self.cursor.execute(sql_isExist,(item['url'],))
            res = self.cursor.fetchall()
            if len(res)>0:
                print('%s 已经存在' % item['url'])
            else:
                self.cursor.execute(sql_insert,(item['school'],item['subjects'], item['years'],item['pnum'],item['time'],item['url']))
                self.connect.commit()
                self.add_num=self.add_num+1
        except Exception as e:
            self.connect.rollback()
            print(e)

        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
        print('更新 %d 条信息！'%self.add_num)

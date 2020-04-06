# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem
import re

class DoubanfilmSpider(scrapy.Spider):
    name = 'doubanfilm'
    headers={
        'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    def __clearInfo(self,texts=[]):
        name =''
        for text in texts:
            if(text!='\n          '):
                name = text[9:-7]
        return name
    def start_requests(self):
        url='https://www.douban.com/doulist/2772079/?start=0&sort=seq&playable=0&sub_type='
        yield scrapy.Request(url=url, headers=self.headers,callback=self.parse)

    def parse(self, response):
        item = [] 
        
        for each in response.xpath('//div[@class="doulist-item"]'): 
            item = TutorialItem()
                       # //*[@id="item14179132"]/div/div[2]/div[3]/a
            try:
                item['name']= self.__clearInfo(each.xpath('.//div[@class="title"]/a/text()').extract())
                item['score']=each.xpath('.//span[@class="rating_nums"]/text()').extract()[0]
                item['country']= each.xpath('.//div[@class="abstract"]/text()').re(r'制片国家/地区: ([\u4e00-\u9fa5]+)')[0]
                item['people_num']=each.xpath('.//div[@class="rating"]/span[3]/text()').extract()[0][1:-5]
                item['time']=each.xpath('.//div[@class="abstract"]/text()').re(r'年份: ([\0-9]{4})')[0]
            except IndexError as e:
                print(e)
                
            print('******************   ********************') 
            print(item)
            print('*****************************************')
            yield item
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            #next_url is list.
            #next_url[0] is str!
            yield scrapy.Request(next_url[0],headers=self.headers,callback=self.parse)

        
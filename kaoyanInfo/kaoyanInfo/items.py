# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KaoyaninfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    school = scrapy.Field()
    subjects = scrapy.Field()
    years = scrapy.Field()
    pnum = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    

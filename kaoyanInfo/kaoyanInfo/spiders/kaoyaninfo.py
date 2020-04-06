# -*- coding: utf-8 -*-
import scrapy
import re

class KaoyaninfoSpider(scrapy.Spider):
    name = 'kaoyaninfo'
    #allowed_domains = ['kao.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Cookie': '_ga=GA1.2.1297771759.1573633641; _emuch_index=1; _last_fid=430; view_tid=14085978; guest_view_tid=14149873; Hm_lvt_2207ecfb7b2633a3bc5c4968feb58569=1585467443,1585476178; _gat=1; Hm_lpvt_2207ecfb7b2633a3bc5c4968feb58569=1585476255'
    }
    def start_requests(self,):
        for n in range(1,389):
            yield scrapy.Request('http://muchong.com/f-430-%d-typeid-2304'%(n),headers=self.headers)
        # yield scrapy.Request('http://muchong.com/f-430-1-typeid-2304',headers=self.headers)

    def parse(self, response):
        #获取页面url
        root_url = 'http://muchong.com'
        for urls in response.xpath('//a[@class="a_subject"]/@href')[1:-1].extract():
            yield scrapy.Request(root_url + urls, headers=self.headers, callback=self.content_parse)
        # url1 = response.xpath('//a[@class="a_subject"]/@href')[1:-1].extract()[0]
        # yield scrapy.Request(root_url + url1, headers=self.headers, callback=self.content_parse)
    def content_parse(self,response):
        item = {}
        
        #item['school'] = response.xpath('//table[@class="adjust_table"/tr[1]/td[2]/text()')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
        try:
            print(response.xpath('//table[@class="adjust_table"]/tr[2]/td[2]/text()').extract()[0])
            item['school'] = response.xpath('//table[@class="adjust_table"]/tr[2]/td[2]/text()').extract()[0]
        except IndexError:
            print('error: 未找到学校名字信息')
            item['school'] = 'error: 未找到学校名字信息'
        
        # print(response.xpath('//table[@class="adjust_table"]/tr[3]/td[2]/text()').extract())
        try:
            #print(response.xpath('//table[@class="adjust_table"]/tr[3]/td[2]/text()').extract())
            subjects = ''
            for s in response.xpath('//table[@class="adjust_table"]/tr[3]/td[2]/text()').extract():    
                pattern = re.compile(r'\s*',re.S)
                strs = pattern.sub('',s)
                if strs!='':
                    subjects = subjects+';'+strs
            subjects = subjects[1:]
            print(subjects)
            item['subjects']=subjects   
        except IndexError:
            print('error: 招生科目有错误！')
            item['subjects']='error: 招生科目有错误！'
        try:    
            #//*[@id="pid1"]/tr[1]/td[2]/div/div[1]/div/table/tbody/tr[4]/td[2]
            print(response.xpath('//table[@class="adjust_table"]/tr[4]/td[2]/text()').extract()[0])
            item['years'] = response.xpath('//table[@class="adjust_table"]/tr[4]/td[2]/text()').extract()[0]
        except IndexError:
            print('error: 年份有错误！')
            item['years'] = 'error: 年份有错误！'
        #//*[@id="pid1"]/tr[1]/td[2]/div/div[1]/div/table/tbody/tr[5]/td[2]
        #//*[@id="pid1"]/tr[1]/td[2]/div/div[2]/div/table/tbody/tr[4]/td[2]
        try:
            print(response.xpath('//table[@class="adjust_table"]/tr[5]/td[2]/text()').extract()[0])
            item['pnum'] = response.xpath('//table[@class="adjust_table"]/tr[5]/td[2]/text()').extract()[0]
        except IndexError:
            print('error: 无法显示招生人数')
            item['pnum']='error: 无法显示招生人数'
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(response.url)
        item['url'] = response.url
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
        #发帖时间
        print(response.xpath('//div[@class="pls_info"]/em/a/text()').extract()[0])
        item['time'] = response.xpath('//div[@class="pls_info"]/em/a/text()').extract()[0]
        #//*[@id="pid1"]/tr[3]/td[1]/div/em/a
        #//*[@id="pid1"]/tr[1]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[2]
        yield item
        
    
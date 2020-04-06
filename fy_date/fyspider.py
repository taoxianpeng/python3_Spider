import requests
from bs4 import BeautifulSoup
from spider import Spider
import json
import time
class FySpyder(Spider):
    def __init__(self):
        pass
    def parse(self):
        html = super().getHtml('http://c.m.163.com/ug/api/wuhan/app/data/list-total') 
        
        title = []
        yesterday_data = []
        
        
        # print(title_time)
        # title.append(title_time)
 
        try:
            data_json = json.loads(html)
            print(data_json['data']['chinaTotal'])
            #数据截至时间
            print(data_json['timestamp'])
            time_local = time.localtime(data_json['timestamp'])
            title_time = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            print(title_time)
        except Exception as e:
            print(e)

    # def parse(self):
    #     html = super().getHtml('https://news.163.com/special/epidemic/') 
    #     bs = super().getBs(html)
    #     title = []
    #     yesterday_data = []
    #     try:
    #         #数据截至时间
    #         title_time = bs.find(class_='cover_time').get_text()[2:-6]
    #         print(title_time)
    #         title.append(title_time)

    #         #疫情数字
    #         cover_data = bs.find_all('div',class_='number')
            
    #         #昨日人数
    #         yd_suspect_num = bs.find('p',class_='added').span.get_text()
    #         yd_confirm_num = re.search(r'confirm: [0-9]*,\n',html).group()[8:-2]
    #         yd_deal_num = re.search(r'dead: [0-9]*,\n',html).group()[6:-2]
    #         yd_heal_num = re.search(r'heal: [0-9]*\n',html).group()[6:-1]
           
    #         yesterday_data.append(yd_confirm_num)
    #         #疑似数据可直接用，不用相减
    #         yesterday_data.append(yd_suspect_num)
    #         yesterday_data.append(yd_deal_num)
    #         yesterday_data.append(yd_heal_num)
    #         # for cover_data_p in cover_data_ps:
    #         #     print(cover_data_p.span.get_text())
  

    #         print(title_time)
    #         for title_p in cover_data:
    #             #if title_p.string != '\n':
    #             title.append(title_p.string)

    #         return (title,yesterday_data)
    #     except Exception as e:
    #         print(e)
        
    
    def customer_parse(self,city):
        html = super().getHtml('https://news.163.com/special/epidemic/') 
        bs = super().getBs(html)
        map_block_mb = bs.find(class_='map_block mb')
        wrap = map_block_mb[1]
        ##test##
        print(wrap)
        
    
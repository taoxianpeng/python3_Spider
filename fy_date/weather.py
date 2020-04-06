from bs4 import BeautifulSoup
import requests
from spider import Spider
class Weather(Spider):
    def __init__(self):
        pass
    def getHtml(self,url):
        # getHtml
        try:
            r = requests.get(url)
            r.encoding='utf-8'
            return r.text
        except Exception as e:
            print(e)
    
    def parse(self):
        html = self.getHtml('http://www.weather.com.cn/weather1d/101250103.shtml') 
        bs = super().getBs(html)
        input_elem = bs.find(id='hidden_title')
        print(input_elem['value'].split(' '))
        weather = input_elem['value'].split(' ')[3]
        tem = input_elem['value'].split(' ')[5]
        return (weather, tem)
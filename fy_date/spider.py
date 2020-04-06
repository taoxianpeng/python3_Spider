from bs4 import BeautifulSoup
import requests
import abc
class Spider(object):

    def getHtml(self,url):
        # getHtml
        try:
            r = requests.get(url,headers={
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'})
            r.close()
            return r.text
        except Exception as e:
            print(e)
    
    def getBs(self,html):
        try:
            bs = BeautifulSoup(html,'lxml') 
            return bs
        except Exception as e:
            print(e)

    @abc.abstractmethod
    def parse(self,bs):
        pass
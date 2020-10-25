import io
import requests
import json
# import re

def getInfor(xuehao):
    url = 'http://wk.byau.edu.cn/default/work/shgcd/jkxxcj/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext'
    cookie = 'route=2f192eae9e39b7d0944957ddc6df793b; default=67A37B79757A40AC9EF5D76EC4CE5B9E; sudyLoginToken=expired'
    UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    
    headers = {
        'User-Agent':UserAgent,
        #cookie过一段时间会失效，暂时无法解决
        'cookie':cookie
    }
    data = {"params":{"empcode":"{}".format(xuehao)},"querySqlId":"com.sudytech.work.shgcd.jkxxcj.jkxxcj.queryNear"}
    try:
        r = requests.post(url,headers=headers,json=data)

        #r.text->str
        return r.text 
    except Exception as e:
        print(e)

def parse(text): 
    pass
if __name__ == "__main__":
    # xuehao = ''
    # for i in range(10,90):
    #     print(xuehao+str(i))
    #     print(getInfor(xuehao+str(i)))
    #     print('\n')
    #20174081302
    text = getInfor('')

    print(text) 
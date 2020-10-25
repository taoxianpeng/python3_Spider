import requests
import time
import logging

def everday_submit():
    everday_submit_url = 'http://wk.byau.edu.cn/poe/_web/_apps/poe/mrdk/api/add.rst?domainId=1'
    header_e_s = {
        'Host': 'wk.byau.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 iPortal/27',
        'X-Requested-With': 'cn.edu.byau.iportal',
        'Referer': 'http://wk.byau.edu.cn/poe/_web/_apps/poe/mrdk/dk.jsp?domainId=1',
        'Cookie': 'SESSION=56d4ecfb-8473-4535-8ccf-1bb5cd50c85f; route=54847d7488245ec0fdffd6293a34cc1a'
    }
    #health_info_submit_url = ''

    try:
        r = requests.post(everday_submit_url,headers=header_e_s)
        return r.text
    except Exception as f:
        print(f)

    return ''
def health_info_submit():
    current = int(time.time()*1000)
    health_info_submit_url = 'http://wk.byau.edu.cn/default/work/shgcd/jkxxcj/com.sudytech.portalone.base.db.saveOrUpdate.biz.ext'
    referer='http://wk.byau.edu.cn/default/work/shgcd/jkxxcj/jkxxcj.jsp?appload=0&f=app&iportal.timestamp={time}&iportal.nonce=3648&iportal.signature=ae5db877b8b7438163df8c8c74a700eada16be1d&iportal.signature2=69630101f92c435440a780cd81e3978f7e2ac5c7&iportal.ip=192.168.1.103&iportal.signature3=177e02ec027b9703c3728627e5b10ba889714c0b&iportal.device=26375ba1ed09dc54f497230e92bceb13&iportal.group=jkxxtbyjsz%2Cyjs&iportal.uid=33033&iportal.uname=%E9%99%B6%E8%B4%A4%E9%B9%8F&iportal.uxid=ZS208247'.format(time=current)
    headers={
        'Host': 'wk.byau.edu.cn',
        'Origin': 'http://wk.byau.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 iPortal/27',
        'Referer': referer,
        'Cookie': 'JSESSIONID=4CC22CF5968BDD466C20C3BC3EDB96B6'
    }
    try:
        r = requests.post(health_info_submit_url,headers=headers)
        return r.text
    except Exception as f:
        print(f)
    return ''

if __name__ == "__main__":
    a = everday_submit()
    print(a)
    b = health_info_submit()
    print(b)
    
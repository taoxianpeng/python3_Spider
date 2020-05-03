import requests
import re
import ctypes
import os

def getPic():
    root_url = 'https://cn.bing.com'
    pic_url = ''
    #获取壁纸的下载地址
    try:
        r = requests.get(root_url)
        pic_url = root_url+re.findall(r'<link id="bgLink" rel="preload" href="([\s\S]+)" as="image" /><link',r.text)[0]
    except Exception as e:
        print(e)

    #下载壁纸到当前文件
    try:
        r2 = requests.get(pic_url)
        with open('wallpaper.jpg','wb') as f:
            f.write(r2.content)
            f.close()
    except Exception as e:
        print(e)

    #设置壁纸
    ctypes.windll.user32.SystemParametersInfoW(20,0,os.getcwd()+'/wallpaper.jpg',0)
    
if __name__ == '__main__':
    getPic()
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import logging
import os
#linux下不能用这个地址
# chromedriver_path = os.getcwd()+'/'+'chromedriver'
#sudo apt install chromium-driver安装
chromedriver_path = '/usr/bin/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO,
                    filename='everdayForm.log',
                    filemode='a')

def run(username, password):
    driver = webdriver.Chrome(chromedriver_path,chrome_options=chrome_options)
    driver.get(r'https://ids.byau.edu.cn/cas/login')
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('passbutton').click()

    cookies = driver.get_cookies()[0]

    driver.add_cookie(cookies)
    driver.get(r'http://wk.byau.edu.cn/default/work/shgcd/jkxxcj/jkxxcj.jsp')

    isFullForm = True
    try:
        driver.find_element_by_id('layui-layer1')
    except NoSuchElementException as e:
        isFullForm = False
    except Exception as f:
        logging.error(username+' - '+f)
 
    if isFullForm:
        # print('当日已经完成填报！')
        logging.info('{username} Today, you filled out of form !'.format(username=username))
    else:
        driver.find_element_by_id('post').click()

    driver.get(r'http://wk.byau.edu.cn/poe/_web/_apps/poe/mrdk/dk.jsp?domainId=1')

    # selenium 执行 js 参考教程
    # https://zhuanlan.zhihu.com/p/159210953

    sleep(2)
    #输入 “出行情况”
    js = "document.getElementById('cxqk').value='no'"
    driver.execute_script(js)
    #点击 checkbox 打勾
    js2 = "document.getElementsByClassName('layui-icon layui-icon-ok')[0].click()"
    driver.execute_script(js2)

    driver.find_element_by_class_name('layui-btn').click()

    if driver.find_element_by_class_name('layui-layer-content').text == '提交后信息无法修改，请确认现在提交？':
        # logging.info('{username} 提交后信息无法修改，请确认现在提交？'.format(username=username))
        driver.find_element_by_class_name('layui-layer-btn0').click()

    sleep(1)
    if driver.find_element_by_class_name('layui-layer-content').text == '已经提交':
        logging.info('{username} Congratuation! you fill out this form! go play.'.format(username=username))

if __name__ == "__main__":
    # username=''
    # password=''
    # run(username,password)
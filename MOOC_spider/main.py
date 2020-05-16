import re
import requests
import os
import random
import urllib

url = 'https://www.icourse163.org/learn/HIT-154005#/learn/content'
dwr_url='https://www.icourse163.org/dwr/call/plaincall/CourseBean.getMocTermDto.dwr'
title = ''

def getHtml(url,pattern='t'):
    try:
        r = requests.get(url)
        if pattern == 't':
            return r.text
        if pattern == 'b':
            return r.content
        else:
            raise Exception('pattern errer')
    except Exception as e:
        print(e)

def getDwr(payload):
    try:
        r = requests.post(dwr_url,data=payload)
        return r.text
    except Exception as e:
        print(e)
    
def main(html):
    global title
    title = re.search(r'<title>\n(\S+)\n</title>',html).group(1) 
    termID = re.search(r'"currentTermId": ([0-9]+),',html).group(1)

    payload='''callCount=1
scriptSessionId=$\{scriptSessionId\}190
c0-scriptName=CourseBean
c0-methodName=getMocTermDto
c0-id=0
c0-param0=number:%s
c0-param1=number:0
c0-param2=boolean:true
batchId=1589443016801
'''%termID

    dwr_text = getDwr(payload)
    parse(dwr_text)

def parse(dwr_text):
    #总共上n周课的集合 -> list
    w = re.findall(r's0\[[0-9]+\]=(s[0-9]+);',dwr_text)
    week_lesson = [] #第N周
    for i in w:
        week_lesson.append(re.search('%s.lessons=(s[0-9]+)'%i,dwr_text).group(1))

    s=[] #二维数组 每周下的课程
    for j in week_lesson:
        s.append(re.findall('%s\[[0-9]+\]=(s[0-9]+)'%j,dwr_text))
    
    sub_lessons = [] #课程 x.x 的 units 中每一小节课
    for k in s:
        for n in k:
            units = re.search('%s.units=(s[0-9]+)'%n,dwr_text).group(1)  
            sub_lessons.append(re.findall('%s\[[0-9]+\]=(s[0-9]+)'%units,dwr_text))
            
    #筛选出 文档的下载页面 提取出contentId
    # .contentType=1 为视频， =3 为文档
    res_list = []
    for e in sub_lessons:
        for f in e:
            contentType = re.search('%s.contentType=([0-9])'%f,dwr_text).group(1)
            if(contentType == '3'):
                # s_id = re.search('%s.id=([0-9]+)'%f,dwr_text).group(1)
                # s_lessonId = re.search('%s.lessonId=([0-9]+)'%f,dwr_text).group(1)
                s_contentId = re.search('%s.contentId=([0-9]+)'%f,dwr_text).group(1)
                res_list.append(s_contentId)
    
    
    # print(sub_lessons)
    # print(res_list)
    for id in res_list:
        download_pdf(id)

def download_pdf(pdf_id):
    #这个url本来是用来请求pdf的地址
    #但是发现，直接用dwr_url也可以请求，所以作废
    #base_url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
    
    #c0-param0 对应 .contentId= 
    #batchId为时间戳（毫秒）
    pdf_payload=('callCount=1\n'
                'scriptSessionId=$\{scriptSessionId\}190\n'
                'httpSessionId=1bf253dff584443eae7b9fe07f5ca35d\n'
                'c0-scriptName=CourseBean\n'
                'c0-methodName=getLessonUnitLearnVo\n'
                'c0-id=0\n'
                'c0-param0=number:%s\n'
                'c0-param1=number:3\n'
                'c0-param2=number:0\n'
                'c0-param3=number:0\n'
                'batchId=1589533485648')%pdf_id
    print(pdf_payload)
    dwr_text = getDwr(pdf_payload)
    pdf_url = re.search(r'textOrigUrl:"(\S+\.pdf)",',dwr_text).group(1)
    pdf_name = urllib.parse.unquote(re.search(r'download=(\S+\.pdf)',dwr_text).group(1))
    
    ad = os.getcwd()+'/'+title #文件夹绝对地址
   
    try:
        r=requests.get(pdf_url)
    except Exception as e:
        print(e)

    #文件夹不存在则新建
    if not os.path.exists(ad):
        os.makedirs(ad)
    #下载pdf
    with open(os.path.join(ad,pdf_name),'wb') as f:
        f.write(r.content)
        f.close()

    print(pdf_name+'......ok')
    
if __name__ == '__main__':
    main(getHtml(url))
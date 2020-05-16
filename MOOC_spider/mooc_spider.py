from re import findall as re_findall,search as re_search
from requests import get,post
from os.path import exists,join
from os import getcwd,makedirs
from urllib.parse import unquote
from tqdm import tqdm

class Mooc_Spider(object):
    url = ''
    dwr_url='https://www.icourse163.org/dwr/call/plaincall/CourseBean.getMocTermDto.dwr'
    title = ''
    id_list=[]
    def __init__(self,url):
        #提取url必要字段
        assert url!=None,'[error]: url is not exist!'
        self.url = re_search(r'https://\S+content',url).group()
        dwr_content = self.getDwr_content(self.getContent(self.url))
        self.id_list = self.parse(dwr_content)


    def getContent(self,url,pattern='t'):
        try:
            r = get(url)
            if pattern == 't': #返回文本
                return r.text
            if pattern == 'b': #返回二进制形式
                return r.content
            else:
                raise Exception('pattern errer')
        except Exception as e:
            print(e)

    def getDwr(self,payload):
        try:
            r = post(self.dwr_url,data=payload)
            return r.text
        except Exception as e:
            print(e)
        
    def getDwr_content(self,html):
        self.title = re_search(r'<title>\n(\S+)\n</title>',html).group(1) 
        termID = re_search(r'"currentTermId": ([0-9]+),',html).group(1)

        payload=('callCount=1\n'
                'scriptSessionId=$\{scriptSessionId\}190\n'
                'c0-scriptName=CourseBean\n'
                'c0-methodName=getMocTermDto\n'
                'c0-id=0\n'
                'c0-param0=number:%s\n'
                'c0-param1=number:0\n'
                'c0-param2=boolean:true\n'
                'batchId=1589443016801')%termID

        dwr_text = self.getDwr(payload)
        return dwr_text

    def parse(self,dwr_text):
        #总共上n周课的集合 -> list
        w = re_findall(r's0\[[0-9]+\]=(s[0-9]+);',dwr_text)
        week_lesson = [] #第N周
        for i in w:
            week_lesson.append(re_search('%s.lessons=(s[0-9]+)'%i,dwr_text).group(1))

        s=[] #二维数组 每周下的课程
        for j in week_lesson:
            s.append(re_findall('%s\[[0-9]+\]=(s[0-9]+)'%j,dwr_text))
        
        sub_lessons = [] #课程 x.x 的 units 中每一小节课
        for k in s:
            for n in k:
                units = re_search('%s.units=(s[0-9]+)'%n,dwr_text).group(1)  
                sub_lessons.append(re_findall('%s\[[0-9]+\]=(s[0-9]+)'%units,dwr_text))
                
        #筛选出 文档的下载页面 提取出contentId
        # .contentType=1 为视频， =3 为文档
        res_list = []
        for e in sub_lessons:
            for f in e:
                contentType = re_search('%s.contentType=([0-9])'%f,dwr_text).group(1)
                if(contentType == '3'):
                    # s_id = re_search('%s.id=([0-9]+)'%f,dwr_text).group(1)
                    # s_lessonId = re_search('%s.lessonId=([0-9]+)'%f,dwr_text).group(1)
                    s_contentId = re_search('%s.contentId=([0-9]+)'%f,dwr_text).group(1)
                    res_list.append(s_contentId)

        #返回pdf文档id的一个list
        return res_list
        
    def get_id_list(self,):
        return self.id_list

    def download_pdf(self,pdf_id):
        #这个url本来是用来请求pdf的地址
        #但是发现，直接用dwr_url也可以请求，所以作废
        #base_url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
        
        #c0-param0=number: 后接上 .contentId= 
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
        
        dwr_text = self.getDwr(pdf_payload)
        pdf_url = re_search(r'textOrigUrl:"(\S+\.pdf)",',dwr_text).group(1)
        pdf_name = unquote(re_search(r'download=(\S+\.pdf)',dwr_text).group(1))
        
        ad = getcwd()+'/'+self.title #文件夹绝对地址
    
        #文件夹不存在则新建
        if not exists(ad):
            makedirs(ad)
        #下载pdf
        pdf_content = self.getContent(pdf_url,'b')
        with open(join(ad,pdf_name),'wb') as f:
            f.write(pdf_content)
            f.close()

        return (pdf_name)
        
if __name__ == '__main__':
    url = input('输入网址:')
    mooc = Mooc_Spider(url)
    
    #进度条显示
    id_list =tqdm(mooc.get_id_list()) 
    for id in id_list:
        a = mooc.download_pdf(id)
        id_list.set_description(a)
    
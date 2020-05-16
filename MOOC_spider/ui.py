from tkinter import *
from tkinter.ttk import *
from mooc_spider import Mooc_Spider
import tkinter.messagebox

class GUI(object):
    def __init__(self,parent):
        self.win = parent
        self.win.title("MOOC 课件下载")    # #窗口标题
        #self.win.
        #self.win.geometry("620x300")   # #窗口位置500后面是字母x

        nScreenWid, nScreenHei = self.win.maxsize()
        nCurWid = 620
        nCurHeight = 300
        self.win.geometry("{}x{}+{}+{}".format(nCurWid, nCurHeight, int(nScreenWid/2 - nCurWid/2), int(nScreenHei/2 - nCurHeight/2)))


        self.f1 = Frame(self.win)
        self.f1.pack(fill=X,pady=3)
        self.label = Label(self.f1, text="网址")
        self.e= Entry(self.f1,shown=None)
        self.label.pack(side=LEFT)
        self.e.pack(side=LEFT,fill=X,padx=5,expand=True)
        self.f2 = Frame(self.win)
        self.f2.pack(fill=X,pady=3)
        self.b1 = Button(self.f2,text='下载',width=10,command=self.run)
        self.b2 = Button(self.f2,text="打开文件夹",width=10,state=DISABLED)
        self.b1.pack(side=LEFT,padx=70)
        self.b2.pack(side=RIGHT,padx=70)
        self.t = Text(self.win,height=15)
        self.t.pack(fill=X,expand=True,pady=3)

        #进度条
        self.f3 = Frame(self.win)
        self.f3.pack(fill=X)
        self.l3 = Label(self.f3,text='process: 0%')
        self.l3.pack(side=LEFT)
        self.p = Progressbar(self.f3,orient='horizontal',length=100,mode='determinate')
        self.p.pack(fill=X,pady=3)              

    def update_progress(self,info):
        self.p['value'] = info['precent']
        self.l3['text'] = 'precess: %d%%'%info['precent']
        self.p.update()
        self.t.insert(END,"完成 ...\t"+info['name']+'\n')
        self.t.see(END) #滚动到最后一行
        self.t.update()

    def run(self):
        url = self.e.get()
        if url != '':
            mooc = Mooc_Spider(url)
            id_list = mooc.get_id_list()
            list_len=len(id_list)
            i=0
            for id in id_list:
                i=i+1
                name = mooc.download_pdf(id)
                precent = int((i/list_len)*100)
                self.update_progress({'name':name,'precent':precent})
            tkinter.messagebox.showinfo('完成','课件已经成功下载！')
        else:
            tkinter.messagebox.showwarning('警告','网址不能为空！')
if __name__ == "__main__":
    parent = Tk()
    GUI(parent)
    parent.mainloop()

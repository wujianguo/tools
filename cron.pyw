#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os,os.path,datetime,shutil,time,urllib,threading,psutil
try:
    import Tkinter
except:
    Tkinter=None
ROOTPATH=os.path.dirname(__file__)
ROOTPATH='D:/backup'
BACKUPDIR=os.path.join(ROOTPATH,'cron_backup')
if not os.path.exists(BACKUPDIR):
    os.mkdir(BACKUPDIR)
BACKUPFILES={'hosts':'C:/Windows/System32/drivers/etc/hosts'}
PROCESS=('YoukuMediaCenter.exe',)
class Tips(threading.Thread):
    def __init__(self,text="Hello World"):
        super(Tips, self).__init__()
        self.text=text
    def run(self):
        if not Tkinter:
            return
        top = Tkinter.Tk()
        top.geometry('400x200')
        label = Tkinter.Label(top,text=self.text)
        label.pack()
        Tkinter.mainloop()
def backupFiles(src,des):
    cur_backdir=os.path.join(des,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    os.mkdir(cur_backdir)
    for f in src:
        if os.path.isfile(src[f]):
            shutil.copy(src[f],os.path.join(cur_backdir,f))
        if os.path.isdir(src[f]):
            shutil.copytree(src[f],os.path.join(cur_backdir,f))
def dingcan(auto=False):
    url="http://dingcan.xunlei.local/dazu/foodquery.jsp?time="+str(time.time()).replace(".",'')
    f=urllib.urlopen(url)
    s=f.read().decode('utf8')
    f.close()
    if s.find(u"吴建国")==-1:
        Tips(u'订餐').start()
def processMonitoring(processes=PROCESS):
    pid=psutil.get_pid_list()
    for i in pid:
        if psutil.Process(i).name in processes:
            Tips(psutil.Process(i).name).start()
def myCron():
    while True:
#        processMonitoring()
        now_time=datetime.datetime.now()
        if now_time.hour==16 and now_time.minute==50:
            dingcan()
            backupFiles(BACKUPFILES,BACKUPDIR)
        time.sleep(60)
if __name__=='__main__':
    myCron()
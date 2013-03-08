#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################
#下载xiami网中所有歌手的热门歌曲，一个歌手最多100首
#从百度下载
#下载一首歌曲： down_one_mp3(歌手名，音乐名，下载到本地的地址)
###############################
import os,os.path,logging,logging.handlers

def init_log():
    py_path=os.path.realpath(__file__)
    log_path=os.path.join(os.path.split(py_path)[0],"log")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_name=os.path.basename(py_path)[0:os.path.basename(py_path).rfind('.')]+".log"
    log_file=os.path.join(log_path,log_name)
    logformat='[%(levelname)s %(asctime)s %(filename)s \
%(module)s %(funcName)s line:%(lineno)d] %(message)s'
    console = logging.StreamHandler()
    stdlog=logging.getLogger("stdlog")
    stdlog.addHandler(console)
    console = logging.handlers.RotatingFileHandler(filename=log_file,
                                                    mode='w',
                                                    maxBytes=20*1024*1024,
                                                    backupCount=20)
    console.setFormatter(logging.Formatter(logformat))
    stdlog.addHandler(console)
    stdlog.setLevel(logging.DEBUG)
init_log()
stdlog=logging.getLogger("stdlog")
import re,urllib
import gevent,signal
import psutil
def down_one_mp3(author_name,song_name,filepath="F:/downloadmusic/"):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    filepath=os.path.join(filepath,author_name)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    try:
        song_url = "http://box.zhangmen.baidu.com/x?op=12&count=1&mtype=1&title="
        song_url=song_url+urllib.quote(song_name.encode('gbk'))
        song_url=song_url+'$$'+urllib.quote(author_name.encode('gbk'))+'$$$$&url=&listenreelect=0&.r=0.1696378872729838'
    
        xmlfile=urllib.urlopen(song_url)
        xml_content=xmlfile.read()
        xml_content=xml_content.decode('gbk')
        url1 = re.findall('<encode>.*?CDATA\[(.*?)\]].*?</encode>',xml_content)
        url2 = re.findall('<decode>.*?CDATA\[(.*?)\]].*?</decode>',xml_content)
    
        url=url1[0][:url1[0].rindex('/')+1] + url2[0]        
        urllib.urlretrieve(url,os.path.join(filepath,song_name+'.mp3'))
    except:
        stdlog.debug(author_name+" "+os.path.join(filepath,song_name)+' error')
    else:
        stdlog.debug(author_name+' '+os.path.join(filepath,song_name)+" down")
def one_page_song(s):
    all=re.findall('class="song_name".*?</a>',s)
    songs=[]
    for one in all:
        song=one[one.rfind('">')+2:one.rfind('</a>')].decode("utf-8")
        songs.append(song)
    return songs
def get_songs(num):
    url="http://www.xiami.com/artist/top/id/"+str(num)+"/page/"
    stdlog.debug(url+str(1))
    songs=[]
    p=urllib.urlopen(url+str(1))
    s=p.read()
    musician=re.compile('id="artist_profile".*?<span>',re.DOTALL).search(s,re.DOTALL)
    if musician:
        musician=musician.group()
    else:
        return "",[]
    musician=musician[musician.rfind('">')+2:musician.rfind('<span>')].decode("utf-8")
    page_num=re.findall('class="p_num"',s)
    songs =songs+one_page_song(s)
    if len(page_num) == 0:
        return musician,songs
    for i in range(2,len(page_num)+2):
        p=urllib.urlopen(url+str(i))
        s=p.read()
        songs =songs+one_page_song(s)
        p.close()
    return musician,songs
def main():
#    gevent.signal(signal.SIGQUIT, gevent.shutdown)
    down_path="F:/xiami_music"
    if not os.path.exists(down_path):
        os.mkdir(down_path)
#    i = 21
#    while True:
    for i in xrange(1,1000):
        musician,songs=get_songs(i)
        if musician=="":
            continue
#        if musician=="" or psutil.disk_usage(down_path).percent > 95:
        if psutil.disk_usage(down_path).percent > 95:
            break
        stdlog.debug(psutil.disk_usage(down_path).percent)
        t=[]
        for song in songs:
            t.append(gevent.spawn(down_one_mp3,musician,song,down_path))
        gevent.joinall(t)
#        i = i+1
if __name__=='__main__':
    main()
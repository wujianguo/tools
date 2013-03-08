#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,os.path,re,platform,logging,logging.handlers
import psutil,urllib,json,time
class show_ip():
    def __init__(self):
        py_path=os.path.realpath(__file__)
        log_path=os.path.join(os.path.split(py_path)[0],"log")
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_name=os.path.basename(py_path)[0:os.path.basename(py_path).rfind('.')]+".log"
        log_file=os.path.join(log_path,log_name)
        logformat='[%(levelname)s %(asctime)s] %(message)s'
        #logging.basicConfig(level=logging.DEBUG)
        
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter("%(asctime)s %(message)s",'%H:%M:%S'))
        self.stdlog=logging.getLogger("stdlog")
        self.stdlog.addHandler(console)
        console = logging.handlers.RotatingFileHandler(filename=log_file,
                                                       mode='a',
                                                       maxBytes=20*1024*1024,
                                                       backupCount=20)
        console.setFormatter(logging.Formatter(logformat))
        self.stdlog.addHandler(console)
        self.stdlog.setLevel(logging.DEBUG)
    def find_pid(self,name=[]):
        pid={}
        pid_list=psutil.get_pid_list()
        for i in pid_list:
            try:
                if psutil.Process(i).name in name or name==[]:
                    pid[i]=psutil.Process(i).name
            except:
                pass
        return pid
        #pid={pid,process_name}
    def is_local_ip(self,ip):
        if not ip:
            return True
        if ip=="0,0,0,0" or\
        ip.startswith("127") or ip.startswith("10") or\
        ip.startswith("172") or ip.startswith("192"):
            return True
        else:
            return False
    def find_remote_ip(self,pid_name):
        remote_ip={}
        for one_pid in pid_name:
            try:
                p=psutil.Process(one_pid)
                for conn in p.get_connections():
                    if conn.remote_address:
                        host=conn.remote_address
                        if not host or len(host)!=2:
                            continue
                        remote_ip[conn]=pid_name[one_pid]
            except:
                pass
        return remote_ip
    def print_addr(self,conn_name):
        
        conn=str(conn_name[0].local_address)+\
        " "+str(conn_name[0].remote_address)+" "+conn_name[0].status+" "+conn_name[1]
        if self.is_local_ip(conn_name[0].remote_address[0]):
            self.stdlog.debug(conn)
            return
        url='http://ip.taobao.com/service/getIpInfo.php?ip='+conn_name[0].remote_address[0]
        ip_info = json.loads(urllib.urlopen(url).read())
        try:
            self.stdlog.debug('%s %s%s%s%s%s%s'%(conn,ip_info['data']['country'],
                                           ip_info['data']['area'],
                                           ip_info['data']['region'],
                                           ip_info['data']['city'],
                                           ip_info['data']['county'],
                                           ip_info['data']['isp']))
        except:
            self.stdlog.debug(conn+":"+str(ip_info))
    def start(self,show_pro=[]):
        self.owned_ip={}
        while True:
            pid_name=self.find_pid(show_pro)
            ip_name=self.find_remote_ip(pid_name)
            for conn in ip_name:
                if conn not in self.owned_ip:
                    self.print_addr((conn,ip_name[conn]))
            self.owned_ip=ip_name
#            time.sleep(0.1)
if __name__=="__main__":
    show_pro=["ThunderPlatform.exe","ThunderServiceLite.exe"]
#    show_pro=["QQ.exe","QQExternal.exe","TXPlatform.exe","QQProtect.exe"]
    my_show_ip=show_ip()

    my_show_ip.start(show_pro)
#    my_show_ip.start()
    if platform.system()=="Windows":
        os.system("pause")

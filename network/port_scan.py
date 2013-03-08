#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,os.path,platform,socket,logging,threading,sys

def scan_ip(ip,min_port,max_port):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(6)
    stdlog=logging.getLogger("stdlog")
    for port in range(min_port,max_port):
        addr=(ip,port)
        try:
            s.connect(addr)
            stdlog.debug(ip+":"+str(port)+" open")
            s.close()
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except:
            pass
    s.close()
    
class Scan(threading.Thread):
    def init(self):
        pass
    def set_cfg(self,ip,min_port,max_port):
        self.ip=ip
        self.min_port=min_port
        self.max_port=max_port
    def run(self):
        scan_ip(self.ip,self.min_port,self.max_port)
    
def scan_ports(ip,min_port,max_port):
    max_thread=300
    step=(max_port-min_port)/max_thread
    if step==0:
        step=min(3,max_port-min_port)
    threads=[]
    for port in range(min_port,max_port,step):
        scan=Scan()
        scan.set_cfg(ip,port,min(port+step,max_port))
        scan.start()
        threads.append(scan)
    for th in threads:
        th.join()
def init_log():
    py_path=os.path.realpath(__file__)
    log_path=os.path.join(os.path.split(py_path)[0],"log")
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_name=os.path.basename(py_path)[0:os.path.basename(py_path).rfind('.')]+".log"
    log_file=os.path.join(log_path,log_name)
    logformat='[%(levelname)s %(asctime)s %(filename)s \
%(module)s %(funcName)s line:%(lineno)d thread:%(thread)d] %(message)s'
    logging.basicConfig(filename=log_file,filemode="w",level=logging.DEBUG,
                        format=logformat)
    console = logging.StreamHandler()
    stdlog=logging.getLogger("stdlog")
    stdlog.addHandler(console)
    
if __name__=='__main__':
    if len(sys.argv)==4:
        ip,min_port,max_port=sys.argv[1:]
    else:
        ip,min_port,max_port=raw_input("ip min_port max_port:").split()
    init_log()
    scan_ports(ip,int(min_port),int(max_port))
    if platform.system()=="Windows":
        os.system("pause")

#! /usr/bin/env python
# -*- coding: utf-8 -*-
HOST = '127.0.0.1'
PORT = 6211
NUM  = 300
import socket
import threading
import SocketServer
import time
class LogClient(threading.Thread):
    def init(self):
        super(LogClient,self).__init__()
    def setfile(self,filepath):
        self.filepath = filepath
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        try:
            f = open(self.filepath,'rb')
            i = 0
            while True:
                d = f.read(1024*256)
                if not d:
                    break
                sock.sendall(d)
                i = i+1
                if i>3:
                    break
                time.sleep(5)
        finally:
            sock.close()
import os

def main():
#    test_dir = 'D:/xltest/video_accelerate/log'
    test_dir = 'E:/temp/TSLOGNewStream'
    threads=[]
    for f in os.listdir(test_dir):
        print(f)
#        if f.startswith('thunder.log'):
        if f.endswith('.log'):
            client=LogClient()
            client.setfile(os.path.join(test_dir,f))
            client.start()
            threads.append(client)
#        break
    for th in threads:
        th.join()
if __name__=='__main__':
    main()
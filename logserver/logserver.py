#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,datetime
import logging,logging.handlers
import threading
from threading import Lock
import socket
import SocketServer
import ConfigParser
import sys
import shutil
__config__ = 'logserver.ini'
ROOT_DIR = sys.path[0]
if not os.path.isdir(ROOT_DIR):
    ROOT_DIR = os.path.split(ROOT_DIR)[0]
#ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
class Common(object):
    """Global Config Object"""

    def __init__(self):
        """load config from logserver.ini"""
#        ConfigParser.RawConfigParser.OPTCRE = re.compile(r'(?P<option>[^=\s][^=]*)\s*(?P<vi>[=])\s*(?P<value>.*)$')
        self.CONFIG = ConfigParser.ConfigParser()
        self.CONFIG_FILENAME = os.path.join(ROOT_DIR,__config__)
        self.CONFIG.read(self.CONFIG_FILENAME)

        self.LISTEN_IP = self.CONFIG.get('server', 'ip') if self.CONFIG.has_option('server', 'ip') else '0.0.0.0'
        self.LISTEN_PORT = self.CONFIG.getint('server', 'port') if self.CONFIG.has_option('server', 'port') else 6210
        
        self.LOG_DIR = self.CONFIG.get('log','dir') if self.CONFIG.has_option('log', 'dir') else 'log'
        if self.LOG_DIR.find(':') == -1 and not self.LOG_DIR.startswith('/'):
            self.LOG_DIR = os.path.join(ROOT_DIR,self.LOG_DIR)
        
        self.LOG_NAME = self.CONFIG.get('log','name') if self.CONFIG.has_option('log', 'name') else 'test.log'
        self.MAXFILESIZE = self.CONFIG.get('log','maxfilesize') if self.CONFIG.has_option('log', 'maxfilesize') else '20*1024*1024'
        self.MAXFILESIZE = eval(self.MAXFILESIZE)
        self.MAXBACKUP = self.CONFIG.getint('log','maxbackup') if self.CONFIG.has_option('log', 'maxbackup') else 20
        self.SEPARATOR = self.CONFIG.get('log','separator') if self.CONFIG.has_option('log', 'separator') else '\\n'
        self.SEPARATOR = self.SEPARATOR.strip().replace('\'','').replace("\"",'')
        self.FORMAT    = self.CONFIG.get('log','format') if self.CONFIG.has_option('log','format') else '%(message)s'
        self.BUFSIZE   = self.CONFIG.get('log','bufsize') if self.CONFIG.has_option('log','bufsize') else '1024*4'
        self.BUFSIZE   = eval(self.BUFSIZE)        
        self.SEPARATOR = eval('\''+self.SEPARATOR+'\'')
        self.DELETELOG = self.CONFIG.getint('log','cleanlog') if self.CONFIG.has_option('log','cleanlog') else 0
        if self.DELETELOG and os.path.exists(self.LOG_DIR):
            try:
                shutil.rmtree(self.LOG_DIR)
            except:
                print('remove dir error')
#        self.LOG_DIR = os.path.join(self.LOG_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        print(self.LOG_DIR)
        self.STDSHOW = self.CONFIG.getint('std','show') if self.CONFIG.has_option('std', 'show') else 0

common = Common()
if not os.path.exists(common.LOG_DIR):
    os.makedirs(common.LOG_DIR)
LOCK = Lock()
console = logging.StreamHandler()
stdlog=logging.getLogger("stdlog")
stdlog.addHandler(console)
stdlog.setLevel(logging.DEBUG)
g_remote_ip = ''
def newLogger():
#    logformat='[%(levelname)s %(asctime)s %(filename)s \
#%(module)s %(funcName)s line:%(lineno)d] %(message)s'
    logformat = common.FORMAT
    global g_remote_ip
    i = 1
    while True:
        thisdir = os.path.join(common.LOG_DIR,datetime.datetime.now().strftime("%Y%m%d%H%M%S_%f_")+g_remote_ip)
        if not os.path.exists(thisdir):
            os.mkdir(thisdir)
        log_file = os.path.join(thisdir,common.LOG_NAME)
        newlog=logging.getLogger(str(i))
        if common.STDSHOW:
            console = logging.StreamHandler()
            newlog.addHandler(console)
            newlog.setLevel(logging.DEBUG)
        console = logging.handlers.RotatingFileHandler(filename=log_file,
                                                        mode='a',
                                                        maxBytes=common.MAXFILESIZE,
                                                        backupCount=common.MAXBACKUP)
        console.setFormatter(logging.Formatter(logformat))
        newlog.addHandler(console)
        newlog.setLevel(logging.DEBUG)
        stdlog.debug(thisdir)
        i = i +1
        ip = yield newlog

logs = newLogger()
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        global g_remote_ip
        LOCK.acquire(True)
        stdlog.debug('%s:%d accept'%self.client_address)
        g_remote_ip = self.client_address[0]
        self.log = logs.next()
        LOCK.release()
        self.data = ''
    def handle(self):
        while True:
            d = self.request.recv(common.BUFSIZE)
            if not d:
                break
            self.data = self.data + d
            i = self.data.find(common.SEPARATOR)
            while i != -1:
                self.log.debug(self.data[:i])
                self.data = self.data[i+len(common.SEPARATOR):]
                i = self.data.find(common.SEPARATOR)
            if len(self.data)>128*1024:
                self.log.debug(self.data)
                self.data = ''
    def finish(self):
        stdlog.debug('%s:%d closed'%self.client_address)
        self.log.debug(self.data)
        self.data = ''
        for h in self.log.handlers:
            self.log.removeHandler(h)
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
def main():
    server = ThreadedTCPServer((common.LISTEN_IP, common.LISTEN_PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
#    server_thread.daemon = True
    server_thread.start()
    stdlog.debug(common.LISTEN_IP + ' ' + str(common.LISTEN_PORT) + '  serving...')
if __name__ == "__main__":
    main()
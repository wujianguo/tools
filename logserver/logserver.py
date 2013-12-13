#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import logging
import logging.handlers
# import threading
from threading import Lock
# import socket
import SocketServer
import json
import sys
import imp

CFG = {}

def newLogger(cfg):
    console_std = logging.StreamHandler()
    stdlog = logging.getLogger("stdlog")
    stdlog.addHandler(console_std)
    stdlog.setLevel(logging.DEBUG)
    client_ip = yield stdlog
    logformat = cfg.get('logformat', '%(message)s')
    while True:
        thisdir = os.path.join(cfg.get('logdir', 'log'), datetime.datetime.now().strftime("%Y%m%d%H%M%S_%f_") + client_ip)
        if not os.path.exists(thisdir):
            os.makedirs(thisdir)
        log_file = os.path.join(thisdir, cfg.get('logname', 'thunder.log'))
        newlog = logging.getLogger(thisdir)
        if cfg.get('stdshow', False):
            # console = logging.StreamHandler()
            newlog.addHandler(console_std)
            newlog.setLevel(logging.DEBUG)
        console = logging.handlers.RotatingFileHandler(
            filename=log_file,
            mode='a',
            maxBytes=cfg.get('maxfilesize', 20 * 1024 * 1024),
            backupCount=cfg.get('maxbackup', 20)
        )
        console.setFormatter(logging.Formatter(logformat))
        newlog.addHandler(console)
        newlog.setLevel(logging.DEBUG)
        stdlog.debug(thisdir)
        client_ip = yield newlog,thisdir


class ThreadedLogRequestHandler(SocketServer.BaseRequestHandler):
    log_lock = Lock()
    CFG = {}
    def setup(self):
        ThreadedLogRequestHandler.log_lock.acquire(True)
        ThreadedLogRequestHandler.CFG['stdlog'].debug('%s:%d accept' % self.client_address)
        self.log,path = ThreadedLogRequestHandler.CFG['logs'].send(self.client_address[0])
        ThreadedLogRequestHandler.log_lock.release()
        self.data = ''
        try:
            name = "analysis"
            fp, pathname, description = imp.find_module(name)
            try:
                self._analysis = imp.load_module(name, fp, pathname, description)
            finally:
                if fp:
                    fp.close()
            # self._analysis = __import__('analysis')
            self._analysis_class = self._analysis.analysis_log(path)
        except:
            self._analysis_class = None

    def handle(self):
        while True:
            d = self.request.recv(ThreadedLogRequestHandler.CFG.get('bufsize', 256 * 1024))
            if not d:
                break
            self.data = self.data + d
            i = self.data.find(ThreadedLogRequestHandler.CFG.get('separator', '\n'))
            while i != -1:
                self.analysis(self.data[:i])
                self.log.debug(self.data[:i])
                self.data = self.data[i + len(ThreadedLogRequestHandler.CFG.get('separator', '\n')):]
                i = self.data.find(ThreadedLogRequestHandler.CFG.get('separator', '\n'))
            if len(self.data) > 128 * 1024:
                self.analysis(self.data)
                self.log.debug(self.data)
                self.data = ''

    def finish(self):
        ThreadedLogRequestHandler.CFG['stdlog'].debug('%s:%d closed' % self.client_address)
        self.analysis(self.data)
        if self._analysis_class:
            try:
                self._analysis_class.close()
            except:
                pass

        self.log.debug(self.data)
        self.data = ''
        for h in self.log.handlers:
            self.log.removeHandler(h)

    def analysis(self, s):
        if self._analysis_class:
            try:
                self._analysis_class.do(s)
            except:
                pass


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def server(host='0.0.0.0', port=6211):
    return ThreadedTCPServer((host, port), ThreadedLogRequestHandler)

def main():
    root_dir = sys.path[0]
    if not os.path.isdir(root_dir):
        root_dir = os.path.split(root_dir)[0]
    os.chdir(root_dir)
    try:
        with open(os.path.join(root_dir, 'logserver.json')) as f:
            CFG = json.load(f)
    except:
        CFG = {}
    print(CFG)
    CFG['logs'] = newLogger(CFG)
    CFG['stdlog'] = CFG['logs'].next()
    ThreadedLogRequestHandler.CFG = CFG

    CFG['stdlog'].debug(CFG.get('ip', '0.0.0.0') + ':' + str(CFG.get('port', 6211)) + '  serving...')
    server(CFG.get('ip', '0.0.0.0'), CFG.get('port', 6211)).serve_forever()
if __name__ == "__main__":
    main()

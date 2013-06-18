#! /usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import SocketServer
import logging
import threading
import os
import re
import shutil
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
HOST = '127.0.0.1'
PORT = 9854
BUF_SIZE = 256*1024
class StreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.error(self.headers)
        file_path = os.path.join(ROOT_DIR, self.path[1:])

        f = self.send_head(file_path)
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        logging.error('xxxxxxxxxxxxxxxxxxx')

    def do_HEAD(self):
        logging.error('do_HEAD,xxxxxxxxx')
        logging.error(self.headers)
        f = self.send_head()
        if f:
            f.close()

    def send_head(self, path):
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", 'application/octet-stream')
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f
    def copyfile(self, source, outputfile):
        while True:
            s = source.read(1024)
            if not s:
                break
            outputfile.write(s)
#        shutil.copyfileobj(source, outputfile)

class ThreadingHTTPServer(SocketServer.ThreadingMixIn,HTTPServer):
    pass

def test():
    os.system('ffplay.exe http://127.0.0.1:9854/right.flv')
def serve_on(handler, host, port = 80):
    serveraddr = (host,port)
    server = ThreadingHTTPServer(serveraddr, handler)
    server.serve_forever()
def main():
#    t = threading.Timer(3.0, test)
#    t.start()
    serve_on(StreamHandler, HOST, PORT)
if __name__=='__main__':
    main()
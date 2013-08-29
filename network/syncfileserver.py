#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler


class ThreadedFileAsynHandler(BaseHTTPRequestHandler):
    def get_dirinfo(self, dirname):
        pass
    def download_file(self, filepath):
    	pass
    def do_GET(self):
        pass
        

class ThreadingHTTPServer(SocketServer.ThreadingMixIn,HTTPServer):
    pass

def server(host='0.0.0.0', port=6231):
    return ThreadingHTTPServer((host, port), ThreadedFileAsynHandler)

def main():
    server().serve_forever()

if __name__ == '__main__':
    main()
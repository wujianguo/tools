#! /usr/bin/env python
# -*- coding: utf-8 -*-
import SocketServer,logging
logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s %(asctime)s line:%(lineno)d] %(message)s')
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        logging.info(self.request.recv(1024))
        self.request.sendall("""<?xml version=\"1.0\"?><cross-domain-policy><site-control permitted-cross-domain-policies=\"all\"/><allow-access-from domain=\"*\" to-ports=\"*\"/></cross-domain-policy>"""+'\x00')
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 843
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import logging
import socket
import select

logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s %(asctime)s line:%(lineno)d] %(message)s')

class SSHPortMappingHandler(SocketServer.StreamRequestHandler):

    def send_all(self, sock, data):
        bytes_sent = 0
        while True:
            r = sock.send(data[bytes_sent:])
            if r < 0:
                return r
            bytes_sent += r
            if bytes_sent == len(data):
                return bytes_sent

    def handle_tcp(self, sock, remote):
        try:
            fdset = [sock, remote]
            while True:
                r, w, e = select.select(fdset, [], [])
                if sock in r:
                    data = sock.recv(4096)
                    if len(data) <= 0:
                        break
                    result = self.send_all(remote, data)
                    if result < len(data):
                        raise Exception('failed to send all data')

                if remote in r:
                    data = remote.recv(4096)
                    if len(data) <= 0:
                        break
                    result = self.send_all(sock, data)
                    if result < len(data):
                        raise Exception('failed to send all data')
        finally:
            sock.close()
            remote.close()

    def handle(self):
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        remote.connect(("192.168.232.128", 22))
        sock = self.connection
        self.handle_tcp(sock, remote)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 6212
    server = ThreadedTCPServer((HOST, PORT), SSHPortMappingHandler)
    server.serve_forever()

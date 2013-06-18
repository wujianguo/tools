#!/usr/bin/env python
# -*- coding: utf-8 -*-

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import struct
import string
import hashlib
import mimetypes
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
HOST = '127.0.0.1'
PORT = 9854
BUF_SIZE = 256*1024
KEY = 'okdoit'
def get_table(key):
    m = hashlib.md5()
    m.update(key)
    s = m.digest()
    (a, b) = struct.unpack('<QQ', s)
    table = [c for c in string.maketrans('', '')]
    for i in xrange(1, 1024):
        table.sort(lambda x, y: int(a % (ord(x) + i) - a % (ord(y) + i)))
    return table
ENCRYPT_TABLE = ''.join(get_table(KEY))
DECRYPT_TABLE = string.maketrans(ENCRYPT_TABLE, string.maketrans('', ''))

def encrypt_file(file_path, encrypt_path):
    rf, wf = open(file_path, 'rb'), open(encrypt_path, 'wb')
    while True:
        data = rf.read(BUF_SIZE)
        if not data:
            break
        wf.write(data.translate(ENCRYPT_TABLE))
    wf.close()
    rf.close()

def decrypt_file(file_path, decrypt_path):
    rf, wf = open(file_path, 'rb'), open(decrypt_path, 'wb')
    while True:
        data = rf.read(BUF_SIZE)
        if not data:
            break
        wf.write(data.translate(DECRYPT_TABLE))
    wf.close()
    rf.close()

class RangeHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        f, start_range, end_range = self.send_head()
        if f:
            f.seek(start_range, 0)
            chunk = 0x1000
            total = 0
            while chunk > 0:
                if start_range + chunk > end_range:
                    chunk = end_range - start_range
                try:
                    if self.encplay(self.path):
                        self.wfile.write(self.decrypt(f.read(chunk)))
                    else:
                        self.wfile.write(f.read(chunk))
                except:
                    break
                total += chunk
                start_range += chunk
            f.close()

    def do_HEAD(self):
        f, start_range, end_range = self.send_head()
        if f:
            f.close()

    def encrypt(self, data):
        return data.translate(ENCRYPT_TABLE)

    def decrypt(self, data):
        return data.translate(DECRYPT_TABLE)

    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return (None, 0, 0)
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return (None, 0, 0)
        if "Range" in self.headers:
            self.send_response(206)
        else:
            self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        size = int(fs[6])
        start_range = 0
        end_range = size
        self.send_header("Accept-Ranges", "bytes")
        if "Range" in self.headers:
            s, e = self.headers['range'][6:].split('-', 1)
            sl = len(s)
            el = len(e)
            if sl > 0:
                start_range = int(s)
                if el > 0:
                    end_range = int(e) + 1
            elif el > 0:
                ei = int(e)
                if ei < size:
                    start_range = size - ei
        self.send_header("Content-Range", 'bytes ' + str(start_range) + '-' + str(end_range - 1) + '/' + str(size))
        self.send_header("Content-Length", end_range - start_range)
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return (f, start_range, end_range)

    def list_directory(self, path):
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return (f, 0, length)

    def translate_path(self, path):
        # abandon query parameters
        encpath = self.encplay(path)
        if encpath:
            return encpath
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def encplay(self, path):
        s = path.split('?',1)
        if len(s) == 2:
            parameters = s[1]
            paras = dict([c.split('=') for c in parameters.split('&')])
            encpath = paras.get('encplay',None)
            if encpath:
                return encpath
        return None
    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        '.mp4': 'video/mp4',
        '.ogg': 'video/ogg',
        })

class ThreadingHTTPServer(SocketServer.ThreadingMixIn,BaseHTTPServer.HTTPServer):
    pass

def serve_on(handler, host, port = 80):
    serveraddr = (host,port)
    server = ThreadingHTTPServer(serveraddr, handler)
    server.serve_forever()
def play(path):
    url = 'http://localhost:'+str(PORT)+'/?encplay='+path
#    url = urllib.quote(url)
    os.system('ffplay '+url)
def main():
    import threading
    t = threading.Timer(1.0, play, ['test.enc'])
    t.start()
    serve_on(RangeHTTPRequestHandler, HOST, PORT)
if __name__=='__main__':
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock
import requests
BUFSIZE = 256*1024

def fs_open(filepath, mode='r', url='', length=0):
	return _fs(filepath, mode, url, length)

class _fs(object):
	def __init__(self, file_path, mode='r', url='', length=0):
		self.lock = Lock()
		self.open(file_path, mode)
	def open(self, file_path, mode='r'):
		self.fobj = open(file_path, mode)
	def read(self, pos, length):
		pass
	def write(self, data, pos=0):
		self.lock.acquire(True)
		self.fobj.write(data)
		self.lock.release()
	def close(self):
		self.fobj.close()

def fetch_range(url, fobj, pos, length):
	print(pos)
	print(length)
	proxies = {'http': 'http://192.168.1.3:9341'}
	headers = {'Range': 'bytes=%s-%s'%(pos, length)}
	r = requests.get(url, headers=headers)
	print(r.headers)
	fobj.write(r.content, pos)
	print(len(r.content))
	print(r.headers['content-length'])
	return int(r.headers['content-length'])
def download(url, filepath):
	r = requests.head(url)
	print(r.headers)
	length = int(r.headers['content-length'])
	f = fs_open(filepath, 'wb', url, length)
	pos = 0
	while length > 0:
		l = fetch_range(url, f, pos, min(BUFSIZE, length))
		pos += l
		length -= l
	f.close()

def main():
	# download('http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.2.zip', '/home/admin/temp/sublime.zip')
	download('https://dl.google.com/chrome/mac/stable/GGRM/googlechrome.dmg', '/home/admin/temp/googlechrome.dmg')
if __name__=="__main__":
	main()
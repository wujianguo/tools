#!/usr/bin/env python
# -*- coding: utf-8 -*-

import worker
# import gevent
# from gevent.threadpool import ThreadPool

def fs_open(file_path, mode='r'):
	return _fs(file_path, mode)
class _fs(object):
	def __init__(self, file_path, mode='r'):
		self.open(file_path, mode)
	def open(self, file_path, mode='r'):
		self.work = worker.workers(1)
		# self.work = ThreadPool(1)
		self.f = open(file_path, mode)
	def read(self, pos, length):
		pass
	def write(self, data, pos=0):
		self.work.apply_async(self._write, pos, data)
	def close(self):
		w = worker.workers(1)
		# w = ThreadPool(1)
		w.apply_async(self._close)
		w.close()
		# w.join()
	def _write(self, pos, data):
		self.f.write(data)
	def _close(self):
		self.work.close()
		self.work.join()
		self.f.close()
def write_one(f):
	s=''
	for i in xrange(1024*256):
		s+='1'
	for i in xrange(1024):
		f.write(s)
def test(files):
	fobjs=[]
	for f in files:
		fob=fs_open(f, 'wb')
		# fob=open(f, 'wb')
		fobjs.append(fob)
		write_one(fob)
	for f in fobjs:
		f.close()
if __name__=="__main__":
	import time
	start=time.clock()
	test(['test1', 'test2'])
	# gevent.wait()
	end=time.clock()
	print(end-start)
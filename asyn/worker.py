#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_thread()
import Queue
import threading
class worker(threading.Thread):
	def __init__(self, queue):
		super(worker, self).__init__()
		self.queue = queue
		self.stop_event = threading.Event()
		self.close_event = threading.Event()
	def run(self):
		while not self.stop_event.isSet():
			try:
				work = self.queue.get(True, 0.01)
				fun = work[0]
				args = work[1]
				kwargs = work[2]
				fun(*args, **kwargs)
			except Queue.Empty:
				if self.close_event.isSet():
					break
	def terminate(self):
		self.stop_event.set()
	def close(self):
		self.close_event.set()
class workers():
	def __init__(self, num=0):
		self.closing = False
		if num==0:
			num = 2
		self.queue = Queue.Queue()
		self.threads = []
		for i in range(num):
			work = worker(self.queue)
			work.start()
			self.threads.append(work)
	def apply_async(self, func, *args, **kwargs):
		if not self.closing:
			self.queue.put((func, args, kwargs))
	def close(self):
		self.closing = True
		for th in self.threads:
			th.close()
	def join(self):
		for th in self.threads:
			th.join()
	def terminate(self):
		for th in self.threads:
			th.terminate()
def test():
	pass
if __name__=="__main__":
	test()
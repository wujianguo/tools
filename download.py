#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib

def download(downurl):
	params={'url':downurl}
	params=urllib.urlencode(params)
	r = requests.post('http://proxy.wujianguo.org', data=params, stream=True)
	f=open(downurl.split('/')[-1], 'wb')
	while True:
		s=r.raw.read(32*1024)
		if not s:
			break
		f.write(s)
	f.close()
def download2(url):
	pass
if __name__=="__main__":
    download2('http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.1.tar.bz2')

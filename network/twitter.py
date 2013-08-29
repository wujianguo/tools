#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib,json,datetime,smtplib
TWITTER_SEARCH_API='http://search.twitter.com/search.json?'
PROXY = {'http': 'http://127.0.0.1:9341'}
def search_twitter(username):
    url = TWITTER_SEARCH_API+'q=from:'+username
    urllib.quote(url)
#    url = 'http://search.twitter.com/search.json?q=%40twitterapi'
    f = urllib.urlopen(url,proxies=PROXY)
    print(json.loads(f.read()))
    f.close()
def print_json(s):
    time_format='%a, %d %b %Y %X'
    
    results = s['results']
    for k in results:
        print(datetime.datetime.strptime(k['created_at'][:-6],time_format))
        print(k['text']+'\n')
def send_email():
    server = smtplib.SMTP('gmail.google.com')
    server.set_debuglevel(1)
    server.sendmail('robot@wujianguo.org', toaddrs, 'hello')
    server.quit()
if __name__=='__main__':
#    search_twitter('kaifulee')
#    f=open('D:/cygwin/home/admin/github/tools/network/search.json')
#    print_json(json.loads(f.read()))
#    f.close()
    send_email()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, requests, os.path, os
MUSIC_DIR = os.path.dirname(os.path.realpath(__file__))
class DoubanFM():
    def login(self,email,passwd):
        payload={'email':email,'password':passwd,'app_name':'radio_desktop_win','version':100}
        url = 'http://www.douban.com/j/app/login'
        r = requests.post(url, data=payload)
        data = r.json
        if data['err']!='ok':
            return False
        self.user_id = data['user_id']
        self.expire = data['expire']
        self.token = data['token']
        return True
    def getSongList(self,channel):
        song_list = []
        print(channel['name'])
        url = 'http://www.douban.com/j/app/radio/people'
        payload = {'app_name':'radio_desktop_win','version':100,'user_id':self.user_id,'expire':self.expire,'token':self.token,'channel':0,'type':'n'}
        r = requests.get(url,params=payload)
        return r.json['song']
    def getChannels(self):
        url = 'http://www.douban.com/j/app/radio/channels'
        r = requests.get(url)
        return r.json['channels']
def main():
    doubanFM = DoubanFM()
    doubanFM.login('','')
    channels = doubanFM.getChannels()
    c = doubanFM.getSongList(channels[0])
    f = open('dd.txt','w')
    for i in c:
        print(i['title'])
#        f.write(i['artist'])
#        f.write(' ')
        f.write(i['url'])
#        f.write(' ')
#        f.write(i['title'])
#        f.write('\n')
    f.close()
if __name__=='__main__':
    main()
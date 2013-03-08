#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,random,time,platform
from datetime import datetime
import pygame
FREQ = 44100
BITSIZE = -16
CHANNELS = 2
BUFFER = 1024
FRAMERATE = 30
def find_music(dir):
    musics=[]
    list_dirs = os.walk(dir)
    for root,dirs,files in list_dirs:
        for f in files:
            if f.endswith(".mp3"):
                musics.append(os.path.join(root,f))
    return musics
def playmusic(soundfile):
    clock = pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(FRAMERATE)
def my_alarm_clock():
    while True:
        now_time=datetime.now()
#        if now_time.hour==8 and now_time.minute==30:
        if now_time.hour==7 and now_time.minute==1:
       # if True:
            play()
        time.sleep(50)
def play():
    if platform.system()=="Windows":
        musics=find_music("E:/music")
    else:
        musics=find_music("/home/justin/Music/chen")
    pygame.mixer.init(FREQ,BITSIZE,CHANNELS,BUFFER)
    for i in range(10):
        playmusic(random.choice(musics))
def main():
    my_alarm_clock()
if __name__=='__main__':
    main()

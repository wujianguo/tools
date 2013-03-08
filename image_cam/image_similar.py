#!/usr/bin/env python
# -*- coding: utf-8 -*-
from VideoCapture import Device
import Image,time,threading
def save_move_image(interval_time):
    cam = Device()
    camshot = cam.getImage()
    while True:
        time.sleep(interval_time)
        camshot2 = cam.getImage()
def make_regular_image(img,size = (256,25)):
    return img.resize(size).convert('RGB')
def hist_similar(lh,rh):
    assert len(lh)==len(rh)
    return sum(1-(0 if l==r else float(abs(l-r))/max(l,r) for l,r in zip(lh,rh)))/len(lh)
def calc_similar(li,ri):
    return hist_similar(li.histogram(),ri.histogram())
def calc_similar_by_path(lf,rf):
    li,ri = make_regular_image(Image.open(lf)),make_regular_image(Image.open(rf))
    return calc_similar(li,ri)
if __name__=='__main__':
    print calc_similar_by_path('D:/t.jpg','D:/t2.jpg')

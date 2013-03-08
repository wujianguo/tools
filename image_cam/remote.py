#!/usr/bin/python
# -*- coding: utf-8 -*-
from VideoCapture import Device
from datetime import datetime
import Image,time

def make_regalur_image(img, size = (256, 256)):
    return img.resize(size).convert('RGB')
def split_image(img, part_size = (64, 64)):
    w, h = img.size
    pw, ph = part_size
    assert w % pw == h % ph == 0
    return [img.crop((i, j, i+pw, j+ph)).copy() \
            for i in xrange(0, w, pw) \
            for j in xrange(0, h, ph)]
def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)
def calc_similar(li, ri):
    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0		
def calc_similar_by_path(lf, rf):
    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
    return calc_similar(li, ri)

def main(s_time=5):
    path1 = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.jpg'
    cam = Device()
    time.sleep(2)
    path2 = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.jpg'
    cam.saveSnapshot(path1)
    for i in range(10):
        time.sleep(s_time)
        cam.saveSnapshot(path2)
        if calc_similar_by_path(path1,path2)<0.8:
            path1 = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.jpg'
        tmp = path2
        path2 = path1
        path1 = tmp
    del cam
    
if __name__ == '__main__':
    s_time = 1
    main(s_time)




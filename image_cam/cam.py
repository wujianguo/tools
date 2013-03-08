#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv
def main():
    cv.NamedWindow("webcam",cv.CV_WINDOW_AUTOSIZE)
    cam=cv.CaptureFromCAM(-1)
    for i in range(10):
        feed=cv.QueryFrame(cam)
        cv.ShowImage("webcam",feed)
        cv.WaitKey(100)
        cv.SaveImage(str(i)+".jpg",feed)
if __name__=='__main__':
    main()

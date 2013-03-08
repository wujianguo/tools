#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,logging,struct,os.path,binascii
#logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s %(asctime)s line:%(lineno)d] %(message)s')
logging.basicConfig(level=logging.DEBUG,format='%(message)s')
FLV_PATH="E:/download/gf/gf/ubuntu_ffmpeg.flv"
#FLV_PATH="E:/download/gf/gf/movie.flv"
AUDIO='AUDIO'
VIDEO='VIDEO'
SCRIPT='SCRIPT'
class FlvDemuxer():
    def __init__(self,flv_path):
        self.flv_path=flv_path
        self.flv_size=os.path.getsize(self.flv_path)
        self.fileobj=open(flv_path,'rb')
        s=self.fileobj.read(9)
        signature, version, _, header_size = struct.unpack("!3sBcI", s)
        assert signature=='FLV'
        self.readPreTagSize()
    def parseAll(self):
        while self.fileobj.tell()<self.flv_size:
            self.flvReadHeader()
            
    def flvReadHeader(self):
        s=self.fileobj.read(8)
        t,size1,size2,timestamp=struct.unpack("!BBHI",s)
        size=(size1<<16)+size2
        timestamp=(timestamp>>8)+((timestamp&0xff)<<24)
        if (t&0x1f)==0x9:
#            pass
            logging.debug(timestamp)
        self.fileobj.seek(3,1)
        if (t&0x1f)==0x8:
            self.fileobj.seek(size,1)
        elif (t&0x1f)==0x9:
            self.fileobj.seek(2,1)
            s=self.fileobj.read(3)
            cpstts=struct.unpack("!BH",s)
            cpstts=(cpstts[0]<<16)+cpstts[1]
#            logging.debug("%d",cpstts)
            self.fileobj.seek(size-5,1)
        elif t&0x1f==0x12:
            self.fileobj.seek(size,1)
        self.readPreTagSize()
    def flvReadPacket(self):
        pass
    def flvReadMetabody(self):
        pass
    def readPreTagSize(self):
        s=self.fileobj.read(4)
        return struct.unpack("!I",s)[0]
    def __del__(self):
        self.fileobj.close()
def main():
    flv_path=FLV_PATH
    if len(sys.argv)==2:
        flv_path=sys.argv[1]
    flv_parse=FlvDemuxer(flv_path)
    flv_parse.parseAll()
    del flv_parse
#    print(binascii.hexlify(s))
if __name__=="__main__":
    main()

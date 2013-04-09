#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from Crypto.PublicKey import RSA
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
__keyname__ = 'id_rsa'
def main():
    key = RSA.generate(1024*2)
    s = key.exportKey()
    with open(os.path.join(ROOT_DIR,__keyname__),'w') as f:
        f.write(s)
    pub = key.publickey()
    s = pub.exportKey()
    with open(os.path.join(ROOT_DIR,__keyname__+'.pub'),'w') as f:
        f.write(s)
if __name__=='__main__':
    main()
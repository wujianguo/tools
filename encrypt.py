#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import md5
import getpass
from Crypto.Cipher import AES

def encrypt_file(file_path ,key, out_path=None):
    if not out_path:
        out_path = file_path+'.enc'
    cipher = AES.new(key, AES.MODE_ECB)
    with open(file_path, 'rb') as f:
        wf = open(out_path, 'wb')
        while True:
            s = f.read(32)
            if len(s)<32:
                s = s + '1' + '0'*(32-len(s)-1)
                wf.write(cipher.encrypt(s))
                break
            wf.write(cipher.encrypt(s))
        wf.close()

def decrypt_file(file_path, key, out_path=None):
    if not out_path:
        out_path = file_path+'.dec'
    cipher = AES.new(key, AES.MODE_ECB)
    with open(file_path, 'rb') as f:
        wf = open(out_path, 'wb')
        last_msg = ""
        while True:
            s = f.read(32)
            if len(s)<32:
                break
            wf.write(last_msg)
            last_msg = cipher.decrypt(s)
        wf.write(last_msg[0:last_msg.rfind('1')])
        wf.close()
def usage():
    pass

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:e:o:hp:', ['help', 'encrypt=', 'decrypt=', 'output='])
    except:
        return usage()
    params = dict(opts)
    k = params.get('-p', None)
    if not k:
        k = getpass.getpass()
    key = md5.new(k)
    key = key.hexdigest()
    if '-e' in params or '--encrypt' in params:
        encrypt_file(params.get('-e', params.get('--encrypt', None)), key, params.get('-o', params.get('--output', None)))
    elif '-d' in params or '--decrypt' in params:
        decrypt_file(params.get('-d', params.get('--decrypt', None)), key, params.get('-o', params.get('--output', None)))
    
if __name__=='__main__':
    main()
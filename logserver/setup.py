#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python setup.py py2exe
from distutils.core import setup
import py2exe
setup(console=['logserver.py'],
    data_files=[('',['logserver.json',]),]
    )
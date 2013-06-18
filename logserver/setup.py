from distutils.core import setup
import py2exe
setup(console=['logserver.py'],
    data_files=[('',['logserver.ini','readme.md']),]
    )
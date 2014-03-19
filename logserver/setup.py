#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python setup.py py2exe
from distutils.core import setup
import py2exe

options = {"py2exe":
			{"compressed": 1,
			"optimize": 2,
			# "ascii": 1,
			# "includes":includes,
			"bundle_files": 2,
			"dll_excludes": ["w9xpopen.exe"]
			}
			}
setup(console=['logserver.py'],
	options = options,
    data_files=[('', ['logserver.json',]),]
    )

# includes = ["PyQt4.QtCore", "PyQt4.QtGui", "sip"] 
# # includes = ["PyQt4", "sip"] 

# options = {"py2exe":
# 			{"compressed": 1,
# 			"optimize": 2,
# 			# "ascii": 1,
# 			"includes":includes,
# 			"bundle_files": 2,
# 			"dll_excludes": ["w9xpopen.exe"]
# 			}
# 			}
# setup(
#     options = options,      
#     zipfile=None, 
#     windows=[{"script": "logserver_gui.pyw", "icon_resources": [(1, "leave.ico")] }],
#     data_files = [('', ['logserver.json', 'leave.ico']),]
#     )
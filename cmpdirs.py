#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import filecmp


def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print(name, dcmp.left, dcmp.right)
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)


def main():
    arg_len = len(sys.argv)
    dir1 = 'E:/android/new_task/jni/common'
    dir2 = 'E:/android/new_task_branch/jni/common'
    if arg_len == 3:
        dir1, dir2 = sys.argv[1:]
        # print(dir1,dir2)
    dcmp = filecmp.dircmp(dir1, dir2)
    print_diff_files(dcmp)
if __name__ == '__main__':
    main()

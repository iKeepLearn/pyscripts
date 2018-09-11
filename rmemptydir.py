#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

def rm_empty(dir_path):
    for root,dirs,files in os.walk(dir_path):
        for dir in dirs:
            fullpath = os.path.join(root,dir)
            try:
                os.rmdir(fullpath)
                print('removed {}'.format(fullpath))
            except OSError as e:
                #print(e)
                continue

if __name__ == '__main__':
    dir_path = sys.argv[-1]
    rm_empty(dir_path)

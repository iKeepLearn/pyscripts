#!/usr/bin/env python
import os, sys
from stat import *

def walktree(top,callback):
    for f in os.listdir(top):
        pathname = os.path.join(top,f)
        mode = os.stat(pathname).st_mode
        try:
            if S_ISDIR(mode):
                walktree(pathname,callback)
            elif S_ISREG(mode):
                callback(pathname)
            else:
                print('Skipping %s' % pathname)
        except:
            continue

def checkpermission(file):
    global mod
    if oct(os.stat(file)[ST_MODE])[-3:] == mod:
        print(file,oct(os.stat(file)[ST_MODE])[-3:])




if __name__ == '__main__':
    path = input('please input path:')
    mod = input('please input you want check files mod(e.g 777):')
    walktree(path,checkpermission)

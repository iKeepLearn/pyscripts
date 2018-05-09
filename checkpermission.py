#!/usr/bin/env python
import os, sys
from stat import *

def walktree(top,callback):
    for f in os.listdir(top):
        pathname = os.path.join(top,f)
        mode = os.stat(pathname).st_mode
        if S_ISDIR(mode):
            walktree(pathname,callback)
        elif S_ISREG(mode):
            callback(pathname)
        else:
            print('Skipping %s' % pathname)

def checkpermission(file):
    print(file,oct(os.stat(file)[ST_MODE])[-3:])


if __name__ == '__main__':
    walktree('/home/san/pypractice',checkpermission)

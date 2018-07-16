#!/usr/bin/env python
import os,sys


def rename(path):
    for root,dirs,files in os.walk(path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.gif'):
                newname = file[0:-4] + '101' + file[-4:]
                oldname = os.path.join(root,file)
                newname = os.path.join(root,newname)
                os.rename(oldname,newname)
                print('{} -> {}'.format(oldname,newname))




if __name__ == '__main__':
    path = sys.argv[-1]
    rename(path)

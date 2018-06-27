#!/usr/bin/env python
import os,sys


def rename(path):
    for root,dirs,files in os.walk(path):
        for file in files:
            print(file)
            if file.endswith('.torrent'):
                newname = file[0:-28] + file[-8:]
                os.rename(file,newname)




if __name__ == '__main__':
    path = sys.argv[-1]
    rename(path)

#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

def getFileList(path):
    path = os.path.abspath(path)
    fileListTmp = os.listdir(path)
    fileList = []
    for i in fileListTmp:
        if i[-3:] == '.ts':
            fileList.append(i)
    fileList.sort(key=lambda x: int(os.path.splitext(x)[0].split('720p')[1]))
    txt = os.path.join(path,'b.txt')
    with open(txt,'w') as f:
        for i in fileList:
            f.write('file ' + str(path) + '/' + i + '\n')

    f.close()
    return txt

def main():
    path = sys.argv[-1]
    txt = getFileList(path)
    outFileName = os.path.abspath(path).split('/')[-1] + '.mp4'
    output = os.path.join(os.path.abspath(path),outFileName)
    os.system('ffmpeg -f concat -safe 0 -i ' + txt + ' -c copy ' + output)
    print('Your video file at {}'.format(output))
    os.system('rm ' + txt)

if __name__ == '__main__':
    main()



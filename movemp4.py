#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os,sys,shutil

def move_mp4(dir_path,target_path):
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            if file.endswith('.mp4') or file.endswith('.MP4'):
                source_file = os.path.join(root,file)
                target_file = os.path.join(target_path,file)
                if source_file != target_file
                    shutil.move(source_file,target_file)
                    print('{} -> {}'.format(source_file,target_file))

if __name__ == '__main__':
    dir_path = sys.argv[-2]
    target_path = sys.argv[-1]
    move_mp4(dir_path,target_path)

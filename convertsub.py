#!/usr/bin/env python3

# -*- coding:utf-8 -*-
import os,sys,shutil

def scan_srt(dir_path,target_path):
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            if file.endswith('.srt'):
                srt_file = os.path.join(root,file)
                html_file = srt_file.replace('srt', 'html')
                convert_srt(srt_file, html_file)
                



def convert_srt(srtfile, htmlfile):
    html = open(htmlfile, 'w')
    with open(srtfile, 'r') as f:
        srt = f.readlines()
    html.write('<h3>TRANSCRIPT</h3>' + '\n')
    for line in srt:
        try:
            int(line)
        except:
            if '>' in line:
                line = line.strip()
                html.write('<h3>' + line + '</h3>' + '\n')
            elif line == '\n':
                html.write('<br/>' + '\n')
            else:
                line = line.strip()
                html.write('<p>' + line + '</p>' + '\n')
                
    html.close()
    
if __name__ == '__main__':
    dir_path = sys.argv[-2]
    target_path = sys.argv[-1]
    scan_srt(dir_path,target_path)
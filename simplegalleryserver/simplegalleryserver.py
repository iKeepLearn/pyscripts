#!/usr/bin/env python

from PIL import Image
import os
import sys
import http.server
import socketserver
import re

def generateThumb(file):
    try:
        im = Image.open(file)
        im.thumbnail((190,90),Image.ANTIALIAS)
        im.save("thumb_" + file)
        thumbfilename = "thumb_" + file
        return thumbfilename
    except:
        return

def scanPath(path='.'):
    IMAGE_FILE_REGEX = '^.+\.(png|jpg|jpeg|tif|tiff|gif|bmp)$'
    for root,dirs,files in os.walk(path):
        image_files = [f for f in files if re.match(IMAGE_FILE_REGEX,f)]
    return image_files


def generateHTML(imglist,imgthumblist):
    with open('div.html','w') as f:
        for x,y in zip(imglist,imgthumblist):
            try:
                f.write('<div data-p="170.00">' + '\n')
                f.write('<img data-u="image" src=' + '"' + x +'"' +'/>' + '\n')
                f.write('<img data-u="image" src=' + '"' + y +'"' +'/>' + '\n')
                f.write('</div>' + '\n')
                #f.write('fuck' + '\n')
            except:
                pass
    f.close()
    filenames = ['htmlhead.html','div.html','htmlfoot.html']
    with open('simplegalleryserver.html','w') as sgs:
        for fname in filenames:
            with open(fname) as f:
                for line in f:
                    sgs.write(line)
            f.close()
    sgs.close()

def run_server():
    #PORT = 8000
    #Handler = http.server.SimpleHTTPRequestHandler
    #httpd = socketserver.TCPServer(('',PORT),Handler)
    #httpd.serve_forever()
    print("Your images at http://127.0.0.1:8000/simplegalleryserver.html")
    os.system('python3 -m http.server')
    

if __name__ == '__main__':
    path = sys.argv[-1]
    imglist = scanPath(path)
    imgthumblist = []
    for i in imglist:
        imgthumblist.append(generateThumb(i))
    generateHTML(imglist,imgthumblist)
    run_server()

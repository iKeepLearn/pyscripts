# -*- coding:utf-8 -*-
import requests
import random
import re
import sys
import os
import getopt

def getHTMLText(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
    try:
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        return r.text
    except requests.exceptions.RequestException as e:
        print(e)

def getURLList(html):
    regex = r"(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)"
    lst = []
    matches = re.finditer(regex, html, re.MULTILINE)
    for x,y in enumerate(matches):
        try:
            lst.append(str(y.group()))
        except:
            continue
    return sorted(set(lst),key = lst.index)

def download(lst,filepath='img'):
    if not os.path.isdir(filepath):
        os.makedirs(filepath)

    filecounter = len(lst)
    filenow = 1
    for url in lst:
        filename = url.split('/')[-1]
        if os.path.isfile(filename):
            filename = str(random.randint(1,1000)) + filename
        print("Downloading {}/{} file name:{}".format(filenow,filecounter,filename.split('/')[-1]))
        os.system('aria2c ' + '-o ' + filename + ' ' + url + ' -d ' + filepath)
        filenow += 1
def usage():
    print("Usage:")
    print(sys.argv[0] + ' -u url -d dir')

def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hu:d:",["help","url=","dir="])
    except getopt.GetoptError as err:
        print('[' + err.opt +']' + err.msg)
        usage()
        sys.exit(2)
    url = None
    filepath = None
    for o,a in opts:
        if o in ('-u','--url'):
            url = a
        elif o in ('-d','--dir'):
            filepath = a
        elif o in ('-h','--help'):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    html = getHTMLText(url)
    lst = getURLList(html)
    download(lst,filepath)

if __name__ == '__main__':
    main()


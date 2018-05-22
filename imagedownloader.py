# -*- coding:utf-8 -*-
import requests
import random
import re
import os

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
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
        filename = filepath +'/' + url.split('/')[-1]
        if os.path.isfile(filename):
            filename = str(random.randint(1,1000)) + os.path.basename(filename)
        with open(filename,'wb') as f :
            try:
                print("Downloading {}/{} file name:{}".format(filenow,filecounter,filename.split('/')[-1]))
                img = requests.get(url,headers=headers)
                img.raise_for_status()
                filenow += 1
                f.write(img.content)
                f.flush()
                f.close()
                print("{} saved".format(filename))
            except requests.exceptions.RequestException as e:
                print(e)
                continue


if __name__ == '__main__':
    url = input('please input the image url:')
    filepath = input('please input the download path:')
    html = getHTMLText(url)
    lst = getURLList(html)
    download(lst,filepath)


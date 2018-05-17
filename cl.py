# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import os

def getHTMLText(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
    r = requests.get(url,headers=headers)
    return r.text

def getURLList(html):
    soup = BeautifulSoup(html,'html.parser')
    lst = []
    img = soup.find_all('img')
    for i in img:
        try:
            href = i.attrs['src']
            lst.append(href)
        except:
            continue
    return lst

def download(lst,filepath='img'):
    if not os.path.isdir(filepath):
        os.makedirs(filepath)

    for url in lst:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
        filename = filepath +'/' + url.split('/')[-1]
        with open(filename,'wb') as f :
            img = requests.get(url,headers=headers)
            f.write(img.content)
            f.flush()
            f.close()


if __name__ == '__main__':
    url = input('please input the image url:')
    filepath = input('please input the download path:')
    html = getHTMLText(url)
    lst = getURLList(html)
    download(lst,filepath)


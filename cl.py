# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
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
    soup = BeautifulSoup(html,'html.parser')
    lst = []
    img = soup.find_all('img')
    for i in img:
        try:
            #href = i.attrs['src'] or i.attrs['data-src']
            if i['src']:lst.append(i.get('src'))
            if i['data-src']:lst.append(i.get('data-src'))
        except:
            continue
    return lst

def download(lst,filepath='img'):
    if not os.path.isdir(filepath):
        os.makedirs(filepath)

    filecounter = len(lst)
    filenow = 1
    for url in lst:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
        filename = filepath +'/' + url.split('/')[-1]
        with open(filename,'wb') as f :
            try:
                img = requests.get(url,headers=headers)
                img.raise_for_status()
                print("Downloading {}/{} file name:{}".format(filenow,filecounter,filename.split('/')[-1]))
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


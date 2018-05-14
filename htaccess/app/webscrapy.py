# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

class Webscrapy():
    def getHTMLText(url,code='utf-8'):
        try:
            urladd = requests.get(url)
            urladd.raise_for_status()
            urladd.encoding = code
            return urladd.text
        except:
            return ''
    def getVideoList(url):
        lst = []
        html = getHTMLText(url)
        soup = BeautifulSoup(html,'html.parser')
        a = soup.find_all('a')
        for i in a:
            try:
                href = i.attrs['href']
                lst.append(re.findall(r"(avi|mpg|mpe|mpeg|asf|wmv|mov|qt|rm|mp4|flv|m4v|webm|ogv|ogg|mkv)",href))
            except:
                continue

    def getVideoList(url):
        lst = []
        html = getHTMLText(url)
        soup = BeautifulSoup(html,'html.parser')
        a = soup.find_all('a')
        for i in a:
            try:
                href = i.attrs['href']
                lst.append(re.findall(r"(mp3|wav|wma|mpa|ram|ra|aac|aif|m4a)",href))
            except:
                continue

    def getImageList(url):
        lst = []
        html = getHTMLText(url)
        soup = BeautifulSoup(html,'html.parser')
        a = soup.find_all('a')
        for i in a:
            try:
                href = i.attrs['href']
                lst.append(re.findall(r"(png|jpg|gif)",href))
            except:
                continue


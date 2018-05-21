#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
import os

class Webscrapy():
    def getHTMLText(self,url):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
        try:
            r = requests.get(url,headers=headers)
            r.raise_for_status()
            return r.text
        except requests.exceptions.RequestException as e:
            print(e)

    def getImageList(self,html):
        regex = r"(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)"
        #lst = []
        matches = re.finditer(regex, html, re.MULTILINE)
        for x,y in enumerate(matches):
            try:
                yield str(y.group())
            except:
                continue
        #return sorted(set(lst),key = lst.index)
    def getVideoList(self,html):
        regex = r"(http(s?):)([/|.|\w|\s|-])*\.(?:avi|mpg|mpe|mpeg|asf|wmv|mov|qt|rm|mp4|flv|m4v|webm|ogv|ogg|mkv)"
        #lst = []
        matches = re.finditer(regex, html, re.MULTILINE)
        for x,y in enumerate(matches):
            try:
                yield str(y.group())
            except:
                continue
        #return sorted(set(lst),key = lst.index)
    def getAudioList(self,html):
        regex = r"(http(s?):)([/|.|\w|\s|-])*\.(?:mp3|wav|wma|mpa|ram|ra|aac|aif|m4a)"
        #lst = []
        matches = re.finditer(regex, html, re.MULTILINE)
        for x,y in enumerate(matches):
            try:
                yield str(y.group())
            except:
                continue
        #return sorted(set(lst),key = lst.index)

    def saveList(self,url,filepath='tmp'):
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        html = getHTMLText(url)
        filename = os.path.join(filepath,url.split('/')[2])
        with open(filename,'w') as f:
            for i in getImageList(html):
                f.write(i + '\n')
            for i in getVideoList(html):
                f.write(i + '\n')
            for i in getAudioList(html):
                f.write(i + '\n')
            f.flush()
            f.close()

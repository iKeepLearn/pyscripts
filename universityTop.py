#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import bs4


def getHTMLText(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    HTMLText = r.text

    return HTMLText

def fillUnivList(ulist,html):
    soup = BeautifulSoup(html,'html.parser')
    for tr in soup.find('tbody').children:
        if isinstance(tr,bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string,tds[1].string,tds[3].string])

def printUnivList(ulist,num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print("{0:^10}\t{1:^20}\t{2:^10}".format('rank','university','total score'))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0],u[1],u[2],chr(12288)))

def main():
    uinfo = []
    url = input('please input url:')
    html = getHTMLText(url)
    fillUnivList(uinfo,html)
    printUnivList(uinfo,20)
main()

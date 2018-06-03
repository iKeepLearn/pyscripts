import re
import os


def getURLList(html):
    regex = r"(http(s?):)([/|.|\w|\s|-])*\.(?:mp4)"
    lst = []
    matches = re.finditer(regex, html, re.MULTILINE)
    for x,y in enumerate(matches):
        lst.append(str(y.group()))
    flist = sorted(set(lst),key=lst.index)

    with open('list.txt','w') as f:
        for i in flist:
            f.write(i + '\n')
    f.close()

if __name__ == '__main__':
    html = open('mitx.html').read()
    getURLList(html)

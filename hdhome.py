#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

class HDHome(object):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"

    def __init__(self,user_agent=user_agent,):
        self.session = requests.Session()
        self.session.headers.update({'user-agent':user_agent})
        self.session.headers.update({'origin':'https://hdhome.org'})
        self.session.headers.update({'referer':'https://hdhome.org/login.php'})

    def login(self,username,password,url='https://hdhome.org/takelogin.php'):
        imagestring = self._get_login_imagestring()
        imagehash = self._get_login_imagehash()
        playload = {'imagestrig':imagestring,
                    'imagehash':imagehash,
                    'username':username,
                    'passowrd':password}
        r = self.session.post(url,playload)
        return self.is_logged_in(r)

    def _get_login_imagestring(self):
        url = 'https://hdhome.org/login.php'
        r = self.session.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        img = soup.find_all("img")
        for i in img:
            if 'image' in i['src']:
                imgurl = 'https://hdhome.org/' + i['src']
                print(imgurl)
        image = self.session.get(imgurl)
        with open('/movie/captcha.png','wb') as f:
            f.write(image.content)
        return self.parse_captcha(image.content)

    def _get_login_imagehash(self):
        url = 'https://hdhome.org/login.php'
        r = self.session.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        imagehash = soup.find("input",{"name":"imagehash"})
        assert imagehash and imagehash['value'],"there is no imagehash on this page"
        return imagehash['value']

    def is_logged_in(self,r,url='https://hdhome.org/index.php'):
        if r:
            r = self.session.get(url)
        return 'Pls keep seeding' in r.text

    def parse_captcha(self,image,threshold=140):
        import re
        from io import BytesIO
        from PIL import Image
        import pytesseract

        image = BytesIO(image)
        image = Image.open(image)

        img = image.convert('L')
        pixdata = img.load()
        w,h = img.size
        for y in range(h):
            for x in range(w):
                if pixdata[x,y] < threshold:
                    pixdata[x,y] = 0
                else:
                    pixdata[x,y] = 255

        regex = r"[\'\"\*~!@#$%^&\+\\n\\r;:,\ ’‘“”]"
        imagestring = pytesseract.image_to_string(img)
        return re.sub(regex,'',imagestring)
    
    def sign(self):
        url = 'https://hdhome.org/attendance.php'
        self.session.headers.update({'referer':'https://hdhome.org/index.php'})
        self.session.headers.update({'upgrade-insecure-requests':'1'})
        r = self.session.get(url,allow_redirects=False)
        return r

def main():
    import time
    from random import randrange
    username = 'hdhome'
    password = 'hdhome'
    hdh = HDHome()
    for i in range(8):
        time.sleep(randrange(5))
        hdh.login(username,password)
        r = hdh.sign()
        if r.status_code == 200:
            break
        else:
            continue

if __name__ == '__main__':
    main()

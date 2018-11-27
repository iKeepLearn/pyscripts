#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import logging
import requests
import pytesseract
from io import BytesIO
from PIL import Image
from urllib.parse import urljoin
from bs4 import BeautifulSoup

logging.basicConfig(filename='ptsign.log',filemode='a',level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S')

class CaptchaParse(object):

    def __init__(self,image):
        self.image = Image.open(image).convert('L')

    def image_to_bin(self,threshold=120):
        pixdata = self.image.load()
        w, h = self.image.size
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return self.image

    def delete_point(self):
        pixdata = self.image.load()
        w,h = self.image.size
        for y in range(1,h-1):
            for x in range(1,w-1):
                count = 0
                if pixdata[x,y-1] > 245:
                    count = count + 1
                if pixdata[x,y+1] > 245:
                    count = count + 1
                if pixdata[x-1,y] > 245:
                    count = count + 1
                if pixdata[x+1,y] > 245:
                    count = count + 1
                if pixdata[x-1,y-1] > 245:
                    count = count + 1
                if pixdata[x-1,y+1] > 245:
                    count = count + 1
                if pixdata[x+1,y-1] > 245:
                    count = count + 1
                if pixdata[x+1,y+1] > 245:
                    count = count + 1
                if count > 6:
                    pixdata[x,y] = 255
        return self.image

    def to_string(self):

        regex = r"[\'\"\*~!@#$%^&\+\\n\\r;:,\ \_\-\)\(’‘“”]"

        image = self.image_to_bin()
        image = self.delete_point()
        imagestring = pytesseract.image_to_string(image)
        imagestring = re.sub(regex,'',imagestring)
        logging.info('imagestring: {}'.format(imagestring))
        return imagestring


class NexusPHP(object):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"

    def __init__(self,url='https://hdhome.org',user_agent=user_agent):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({'user-agent':user_agent})
        self.session.headers.update({'origin':self.url})
        self.session.headers.update({'referer':urljoin(self.url,'login.php')})

    def login(self,username,password):
        url=urljoin(self.url,'takelogin.php')
        imagestring = self._get_login_captcha()[0]
        imagehash = self._get_login_captcha()[1]
        playload = {'imagestrig':imagestring,
                    'imagehash':imagehash,
                    'username':username,
                    'password':password}
        if len(imagestring) == 6:
            r = self.session.post(url,playload,timeout=6)
            logging.info('get {} code {}'.format(url,str(r.status_code)))
        return self.is_logged_in(r)


    def _get_login_captcha(self):
        url = urljoin(self.url,'login.php')
        r = self.session.get(url,timeout=6)
        soup = BeautifulSoup(r.text,"html.parser")


        img = soup.find_all("img")
        for i in img:
            if 'image' in i['src']:
                imgurl = urljoin(self.url,i['src'])
        image = self.session.get(imgurl)
        image = BytesIO(image.content)
        image = CaptchaParse(image)
        imagestring = image.to_string()

        imagehash = soup.find("input",{"name":"imagehash"})
        assert imagehash and imagehash['value'],"there is no imagehash on this page"
        logging.info('imagehash: {}'.format(imagehash['value']))
        return (imagestring,imagehash['value'])

    def is_logged_in(self,r):
        url=urljoin(self.url,'index.php')
        if r:
            r = self.session.get(url,timeout=6)
        return 'Pls keep seeding' in r.text

    def sign(self):
        url = urljoin(self.url,'attendance.php')
        self.session.headers.update({'referer':urljoin(self.url,'index.php')})
        self.session.headers.update({'upgrade-insecure-requests':'1'})
        r = self.session.get(url,allow_redirects=False,timeout=6)
        logging.info('get {} code {}'.format(url,str(r.status_code)))
        return r

def main():
    import time
    from random import randrange
    username = 'hdhome'
    password = 'hdhome'
    gzt = NexusPHP('https://pt.gztown.net')
    for i in range(1,8):
        time.sleep(randrange(5))
        logging.info('{} times trying'.format(i))
        gzt.login(username,password)
        time.sleep(randrange(5))
        r = gzt.sign()
        if r.status_code == 200:
            logging.info('sign success')
            break
        else:
            logging.info('sign failure')
            continue

if __name__ == '__main__':
    main()

#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import os,sys
import ssl,socket
import time
from datetime import datetime
import requests

DOMAIN_FILE = "domain.txt"
SERVER_CHAN_KEY = ""
ALERT_DAYS = 5

def is_domain(domain):
    is_domain = False
    regex = r'(^[0-9a-zA-Z][0-9a-zA-Z_]+)\.([a-zA-Z]+)'
    is_domain = bool(re.match(regex,str(domain)))
    if not is_domain:
        print("{} is not a domain".format(domain))
    return is_domain


def get_ssl_info(domain):
    server_name = domain
    print("get ssl information for {}".format(domain))
    sslinfo = {}

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()

    s = socket.socket()
    s.settimeout(5)
    s = context.wrap_socket(s,server_hostname=server_name)
    try:
        s.connect((server_name,443))
        s.do_handshake()
        cert = s.getpeercert()

        e_time = ssl.cert_time_to_seconds(cert['notAfter'])
        remain = e_time
        e_time = datetime.utcfromtimestamp(e_time)

        s_time = ssl.cert_time_to_seconds(cert['notBefore'])
        s_time = datetime.utcfromtimestamp(s_time)

        check_time = datetime.utcnow()

        sslinfo['check_time'] = str(check_time)
        sslinfo['domain'] = server_name
        sslinfo['s_time'] = str(s_time)
        sslinfo['e_time'] = str(e_time)
        sslinfo['remain'] = remain

        return sslinfo
    except socket.timeout:
        print("TimeOut")

def add_from_file(file):
    with open(file,'r') as f:
        for i in f.readlines():
            sslinfo = get_ssl_info(i.strip())
            remain = sslinfo["remain"] - time.time()
            remain = round(remain/86400)
            if remain <  ALERT_DAYS:
                message = "{} ssl certificate have {} days, expire time is {}.".format(sslinfo["domain"], remain,sslinfo["e_time"])
                key = SERVER_CHAN_KEY
                send_alert_message(key,message)
                time.sleep(3)



def send_alert_message(key,message):
    params = {"text":"SSL ALERT","desp":message}
    url = "https://sc.ftqq.com/{}.send".format(key)
    requests.get(url,params=params)

def main():
    add_from_file(DOMAIN_FILE)


if __name__ == '__main__':
    main()


# -*- coding:utf-8 -*-

import re
import requests
from copy import deepcopy
from bs4 import BeautifulSoup
from subprocess import Popen,PIPE

class Acme(object):

    @staticmethod
    def get_challenge(domain):
        challenge_text = Popen(["/home/san/.acme.sh/acme.sh","--issue","-d",domain,"--dns",
                                "--yes-I-know-dns-manual-mode-enough-go-ahead-please"],
                                stdout=PIPE)
        txt_value = challenge_text.communicate()[0]
        txt_value = deepcopy(txt_value.decode())
        regex = r"[(\'\w\')|(\'\w\-\')]{20,60}"
        txt_value = re.search(regex,txt_value).group()
        return re.sub('\'','',txt_value)


    @staticmethod
    def renew(domain):
        renew_output = Popen(["/home/san/.acme.sh/acme.sh","--renew","-d",domain,
                                "--yes-I-know-dns-manual-mode-enough-go-ahead-please"],
                                stdout=PIPE)
        cert_path = renew_output.communicate()[0]
        cert_path = deepcopy(cert_path.decode())
        regex = r"[\'\w\-\']{30,50}"
        cert_path = re.search(regex,cert_path).group()
        return re.sub('\'','',cert_path)


class Freenom(object):

    def __init__(self,user_agent):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        self.session.headers.update({'Host': 'my.freenom.com'})
        self.session.headers.update({'Referer': 'https://my.freenom.com/clientarea.php'})

     def login(self, username, password, url="https://my.freenom.com/dologin.php"):
         token = self._get_login_token()
         playload = {'token': token,
                     'username': username,
                     'password': password}
         r = self.session.post(url, playload)
         assert r, "couldn't get %s" % url
         return r.status_code

    def update_record(self, domain,records=None):

        domain_id = self._get_domain_id(domain)
        url = "https://my.freenom.com/clientarea.php?managedns={}&domainid={}".format(domain,domain_id)
        token = self._get_manage_domain_token(url)
        record_id = self._get_record_id(domain)
        action = 'modify' if record_id else 'add'
        playload = {
             'dnsaction': action,
             'token': token
         }
        playload[record_id + "[name]"] = str(record.name)
        playload[record_id + "[type]"] = record.type.name
        playload[record_id + "[ttl]"] = str(record.ttl)
        playload[record_id + "[value]"] = str(record.target)
        playload[record_id + "[priority]"] = ""
        playload[record_id + "[port]"] = ""
        playload[record_id + "[weight]"] = ""
        playload[record_id + "[forward_type]"] = "1"

        r = self.session.post(url, data=playload)


    def _get_token(self, url):
        r = self.session.get(url)
        assert r, "couldn't get %s" % url
        soup = BeautifulSoup(r.text, "html.parser")
        token = soup.find("input", {'name': 'token'})
        assert token and token['value'], "there's no token on this page"
        return token['value']

    def _get_domain_id(self,domain):
        url = 
        r = self.session.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        
        return domain_id
    
    def _get_domain_id(self,domain):
        url = 
        r = self.session.get(url)
        soup = BeautifulSoup(r.txt,'html.parser')

        return domain_id

    def _get_login_token(self, url="https://my.freenom.com/clientarea.php"):
        return self._get_token(url)

    def _get_domain_token(self, url='https://my.freenom.com/clientarea.php?action=domains'):
        return self._get_token(url)
    
    def _get_manage_domain_token(self, url):
        return self._get_token(url)

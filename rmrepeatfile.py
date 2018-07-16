#! /bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import hashlib

def md5sum(file):
    return hashlib.md5(file.encode('utf-8')).hexdigest()

def main():
    file = 'imageme.py'
    print(md5sum(file))

if __name__ == '__main__':
    main()


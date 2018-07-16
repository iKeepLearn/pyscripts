#! /bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import hashlib
import os
import sys

def md5sum(file):
    md5_hash = hashlib.md5()
    with open(file,"rb") as f:
        for byte_block in iter(lambda:f.read(65536),b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def create_hash_table():
    if os.path.isfile('filehash.db'):
        os.unlink('filehash.db')
    conn = sqlite3.connect('filehash.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE FILEHASH
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FILE TEXT NOT NULL,
            HASH TEXT NOT NULL);''')
    conn.commit()
    c.close()
    conn.close()

def insert_hash_table(file):
    conn = sqlite3.connect('filehash.db')
    c = conn.cursor()
    md5 = md5sum(file)
    c.execute("INSERT INTO FILEHASH (FILE,HASH) VALUES (?,?);",(file,md5))
    conn.commit()
    c.close()
    conn.close()

def scan_files(dir_path):
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            filename = os.path.join(root,file)
            insert_hash_table(filename)

def del_repeat_file(dir_path):
    conn = sqlite3.connect('filehash.db')
    c = conn.cursor()
    for root,dirs,files in os.walk(dir_path):
        print('scanning {} ...'.format(root))
        for file in files:
            filename = os.path.join(root,file)
            md5 = md5sum(filename)
            c.execute('select * from FILEHASH where HASH=?;',(md5,))
            total = c.fetchall()
            removed = 0
            if len(total) >= 2:
                os.unlink(filename)
                removed += 1
                print('{} removed'.format(filename))
                c.execute('delete from FILEHASH where HASH=? and FILE=?;',(md5,filename))
                conn.commit()

    conn.close()
    print('removed total {} files.'.format(removed))



def main():
    dir_path = sys.argv[-1]
    create_hash_table()
    scan_files(dir_path)
    del_repeat_file(dir_path)

if __name__ == '__main__':
    main()


#! /bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import hashlib
import os
import sys

def md5sum(file):
    md5_hash = hashlib.md5()
    try:
        with open(file,"rb") as f:
            for byte_block in iter(lambda:f.read(65536),b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    except IOError as e:
        print(e)
        pass

def create_hash_table():
    if os.path.isfile('filehash.db'):
        os.unlink('filehash.db')
    conn = sqlite3.connect('filehash.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE FILEHASH
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FILE TEXT ,
            HASH TEXT );''')
    conn.commit()
    c.close()
    conn.close()

def insert_hash_table(file):
    conn = sqlite3.connect('filehash.db')
    conn.text_factory = str
    c = conn.cursor()
    md5 = md5sum(file)
    c.execute("INSERT INTO FILEHASH (FILE,HASH) VALUES (?,?);",(file,md5))
    conn.commit()
    c.close()
    conn.close()

def scan_files(dir_path):
    for root,dirs,files in os.walk(dir_path):
        print('create hash table for {} files ...'.format(root))
        for file in files:
            filename = os.path.join(root,file)
            insert_hash_table(filename)

def del_repeat_file(dir_path):
    conn = sqlite3.connect('filehash.db')
    c = conn.cursor()
    removed = 0
    for root,dirs,files in os.walk(dir_path):
        print('scan repeat files {} ...'.format(root))
        for file in files:
            filename = os.path.join(root,file)
            md5 = md5sum(filename)
            c.execute('select * from FILEHASH where HASH=?;',(md5,))
            total = c.fetchall()
            if len(total) >= 2:
                os.unlink(filename)
                removed += 1
                print('{} removed'.format(filename))
                c.execute('delete from FILEHASH where HASH=? and FILE=?;',(md5,filename))
                conn.commit()

    conn.close()
    print('removed total {} files.'.format(removed))

def write_to_file():
    conn = sqlite3.connect('filehash.db')
    c = conn.cursor()
    c.execute('select * from FILEHASH;')
    rows = c.fetchall()
    with open('filehash.txt','w') as f:
        for row in rows:
            line = str(row).replace('(','')
            line = line.replace(')','')
            line = line.replace('u','')
            line = line.replace("'","")
            line = line.replace(',','|')
            f.write(line + '\n')
    c.close()
    conn.close()
    f.close()
    print('Your file md5 hash in filehash.txt')


def main():
    dir_path = sys.argv[-1]
    cmd = sys.argv[-2]
    if cmd == "scan":
        create_hash_table()
        scan_files(dir_path)
        write_to_file()
    elif cmd == "del":
        create_hash_table()
        scan_files(dir_path)
        del_repeat_file(dir_path)
    else:
        print("usage: scan|del dirpath")

if __name__ == '__main__':
    main()


#!/usr/bin/env python3

import os
import sys
import getpass
import hashlib
import argparse

def md5sum(file):
    md5_hash = hashlib.md5()
    try:
        with open(file, 'rb') as f:
            for byte in iter(lambda:f.read(65536), b''):
                md5_hash.update(byte)
        return md5_hash.hexdigest()
    except IOError as e:
        print(e)
        pass

def generate_password(src, user, key, length=12):
    password = hashlib.sha256((src + user + key).encode()).hexdigest()
    password = password[0:length]
    return password


class ClipBoard():

    @staticmethod
    def copy(message):
        platform = sys.platform
        if 'win32' in  platform or 'cyg' in platform:
            cmd = 'echo {}|clip'.format(message)
        elif 'linux' in platform:
            cmd = 'echo {}|xclip'.format(message)
        os.system(cmd)

class GetKey(argparse.Action):
    def __init__(self, option_strings, dest=None, nargs=0, default=None, required=False, type=None, metavar=None, help=None):
        super(GetKey, self).__init__(option_strings=option_strings, dest=dest, nargs=nargs, default=default, required=required, type=type, metavar=metavar, help=help)
    def __call__(self, parser, args, values, option_strings=None):
        key = getpass.getpass("key or file path:")
        setattr(args, self.dest, key)


def main():
    parser = argparse.ArgumentParser(description="generate password")
    parser.add_argument("src", help="target")
    parser.add_argument("user", help="username")
    parser.add_argument("key", action=GetKey, help="the encypt key of file")
    parser.add_argument("-l", dest='length', type=int, default=12, required=False, help="the length of password")
    parser.add_argument("-c", dest="copy", action="store_true", default=False, required=False, help="copy to clipboard")
    args = parser.parse_args()

    src = args.src
    user = args.user
    key = args.key
    length = args.length
    copy = args.copy

    if os.path.isfile(key):
        key = md5sum(key)

    password = generate_password(src, user, key, length)
    if copy:
        ClipBoard.copy(password)
    else:
        print(password)

if __name__ == '__main__':
    main()

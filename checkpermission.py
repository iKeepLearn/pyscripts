#!/usr/bin/env python3

import click
import os
from stat import *

def check_file(file,mod):
    if oct(os.stat(file)[ST_MODE])[-3:] == str(mod):
        print(file,oct(os.stat(file)[ST_MODE])[-3:])

@click.command()
@click.argument('path')
@click.option('--mod','-m',help="The file mode " )
def checkpermission(path,mod=777):
    for root,dirs,files in os.walk(path):
        for file in files:
            try:
                file = os.path.join(root,file)
                check_file(file,mod)
            except:
                continue


if __name__ == '__main__':
    checkpermission()

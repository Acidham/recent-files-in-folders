#!/usr/bin/python
import os
import shutil
import sys

from Alfred import Tools


def remove(p):
    if os.path.isfile(p):
        os.remove(p)
    elif os.path.isdir(p):
        shutil.rmtree(p)
    elif os.path.islink(p):
        os.unlink(p)


HOME = os.path.expanduser('~')
query = Tools.getArgv(1)
root = os.path.join(HOME, query)

for it in os.listdir(root):
    if it != ".DS_Store" and it != "Icon\r":
        it_path = os.path.join(root, it)
        remove(it_path)
sys.stdout.write(root)

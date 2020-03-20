#!/usr/bin/python
import os
import sys

from Alfred import Tools


def remove(p):
    if os.path.isdir(it_path):
        os.removedirs(it_path)
    elif os.path.islink(it_path):
        os.unlink(it_path)
    else:
        os.remove(it_path)


HOME = os.path.expanduser('~')

query = Tools.getArgv(1)

root = "{0}/{1}".format(HOME, query)

for it in os.listdir(root):
    if it != ".DS_Store" and it != "Icon\r":
        it_path = os.path.join(root, it)
        remove(it_path)
sys.stdout.write(root)

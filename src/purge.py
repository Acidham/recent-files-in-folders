#!/usr/bin/env python3
import os
import shutil
import sys

from Alfred3 import Tools


def remove(p):
    if os.path.isfile(p):
        os.remove(p)
    elif os.path.isdir(p):
        shutil.rmtree(p)
    elif os.path.islink(p):
        os.unlink(p)


f_path = Tools.getArgv(1)

# Purge directory, excl. System files
for it in os.listdir(f_path):
    if it != ".DS_Store" and it != "Icon\r":
        it_path = os.path.join(f_path, it)
        remove(it_path)
sys.stdout.write(f_path)

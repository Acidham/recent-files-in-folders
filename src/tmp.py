#!/usr/bin/python

import sys

from Alfred import Tools

f = Tools.getDataDir()
sys.stderr.write(f)

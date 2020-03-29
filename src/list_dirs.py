#!/usr/bin/python

import json
import os

from Alfred import Items, Tools

query = Tools.getArgv(1)
wf_data_dir = Tools.getDataDir()
config_file = os.path.join(wf_data_dir, "folders.json")
wf = Items()
if os.path.isfile(config_file):
    with open(config_file, "r") as f:
        config = json.load(f)
    # List Folders from folders.json
    if len(config.keys()) > 0:
        for k, v in config.items():
            if os.path.isdir(v) and (query == str() or k.lower().startswith(query.lower())):
                wf.setItem(
                    title=k,
                    subtitle=u"\u23CE to list Files or \u2318 for addtional actions",
                    arg=v
                )
                wf.addMod(
                    key="cmd",
                    arg=v,
                    subtitle="Enter Action Menu"
                )
                wf.addModsToItem()
            elif not(os.path.isdir(v)):
                wf.setItem(
                    title=k,
                    subtitle="Folder not found!",
                    arg=k
                )
                wf.setIcon("attention.png", "image")
            wf.addItem()
    else:
        wf.setItem(
            title="Folder configuration is empty",
            subtitle="Add folder via File Action",
            valid=False
        )
        wf.setItem('attention.png', 'image')
        wf.addItem()
else:
    wf.setItem(
        title="Add Folder(s) to config",
        subtitle="Your run WF for the first time, please add folder(s) via file action first",
        valid=False
    )
    wf.setIcon("attention.png", 'image')
    wf.addItem()

wf.write()

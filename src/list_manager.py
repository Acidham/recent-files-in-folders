#!/usr/bin/python

import json
import os
import sys

from Alfred import Tools

wf_data_dir = Tools.getDataDir()
config_file = os.path.join(wf_data_dir, 'folders.json')
if os.path.isfile(config_file):
    with open(config_file, "r") as f:
        config = json.load(f)
else:
    config = dict()

query = Tools.getArgv(1).split('|')
if len(query) > 1:
    target_dir = query[0]
    action = query[1]
else:
    target_dir = query[0]
    action = "ADD"


target_name = os.path.basename(target_dir)

if action == "ADD":
    config.update({target_name: target_dir})
else:
    new_config = dict()
    for k, v in config.items():
        if k != target_name:
            new_config.update({k: v})
    config = new_config

# Remove config before saving changes
os.path.isfile(config_file) and os.remove(config_file)
with open(config_file, 'w') as f:
    f.write(json.dumps(config, indent=2))

if os.path.isfile(config_file):
    sys.stdout.write("Configuration saved")
else:
    sys.stdout.write("Cannot write config file")

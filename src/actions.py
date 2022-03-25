#!/usr/bin/env python3

from Alfred3 import Items, Tools

target_dir = Tools.getEnv('directory')

wf = Items()
# Back Item
wf.setItem(
    title="BACK",
    subtitle="Back to List",
    arg='{0}|{1}'.format(target_dir, "BACK")
)
wf.setIcon(
    m_path="back.png",
    m_type="image"
)
wf.addItem()

# Purge Dir Item
wf.setItem(
    title="Purge Directory",
    subtitle='Purge "{}"'.format(target_dir),
    arg='{0}|{1}'.format(target_dir, "PURGE")
)
wf.setIcon(
    m_path="purge.png",
    m_type="image"
)
wf.addItem()

# Delete Item
wf.setItem(
    title="Remove Folder entry",
    subtitle='Remove "{}" from configuration'.format(target_dir),
    arg='{0}|{1}'.format(target_dir, "DELETE")
)
wf.setIcon(
    m_path="delete.png",
    m_type="image"
)
wf.addItem()

wf.write()

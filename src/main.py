#!/usr/bin/python

import os
import sys
from collections import namedtuple
import Alfred


class RecentFiles:

    def __init__(self,path='/'):
        self.path = path

    def getRecentFiles(self,reverse=True):
        err = 0
        try:
            file_list = os.listdir(self.path)
        except OSError as e:
            err = e.errno
            pass
        if err == 0:
            FileList = namedtuple('FileList', 'filename path time')
            seq = list()
            for f in file_list:
                f_path = self.path + '/' + f
                os.stat_float_times(True)
                file_stats = os.stat(f_path)
                f_time = file_stats.st_ctime

                not(f.startswith('.')) and seq.append(FileList(filename=f, path=f_path, time=f_time))

            seq.sort(key=lambda x: getattr(x, 'time'), reverse=reverse)

            ret_dict = dict()
            i = 0
            for nt in seq:
                nt_d = nt._asdict()
                ret_dict.update({i: {'filename': nt_d['filename'], 'path':nt_d['path']}})
                i = i + 1
            return ret_dict


query = sys.argv[1]
query = str(query).replace(':','/')
if not(str(query).startswith('/')):
    u_dir = os.path.expanduser('~')
    query = u_dir + '/' + query


rf = RecentFiles(query)
seq = rf.getRecentFiles(reverse=True)

wf = Alfred.Items()
if seq is not None:
    for _,d in seq.items():
        wf.setItem(
            title=d['filename'],
            subtitle='Press ENTER to open...',
            arg=d['path'],
            quicklook=d['path']
        )
        wf.setIcon(d['path'],'fileicon')
        wf.addItem()
else:
    wf.setItem(
        title='Path not found...',
        subtitle='Change path in List Filter, e.g. /Users/<user>/Desktop',
        valid=False
    )
    wf.setIcon('attention.png','png')
    wf.addItem()

output = wf.getItems(d_type='json')
sys.stdout.write(output)

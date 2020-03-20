#!/usr/bin/python

import math
import os

from Alfred import Items as Items
from Alfred import Tools as Tools


class RecentFiles:

    def __init__(self, path=str()):
        self.path = path

    def getRecentFiles(self, reverse=True):
        """
        Get list of files in directory as dict
        :param reverse: bool
        :return: list(dict())
        """
        err = 0
        try:
            file_list = os.listdir(self.path)
        except OSError as e:
            err = e.errno
            pass
        if err == 0:
            seq = list()
            for f in file_list:
                f_path = "{0}/{1}".format(self.path, f)
                os.stat_float_times(True)
                file_stats = os.stat(f_path)
                f_time = file_stats.st_birthtime
                f_size = file_stats.st_size

                not (f.startswith('.') or f.endswith('\r')) and seq.append({
                    'filename': f,
                    'path': f_path,
                    'time': f_time,
                    'size': f_size
                })
            sorted_file_list = sorted(
                seq, key=lambda k: k['time'], reverse=reverse)
            return sorted_file_list

    def getRecentFilesDeep(self, reverse=True):
        """
        Get list of files in directory as dict
        :param reverse: bool
        :return: list(dict())
        """
        err = 0
        try:
            file_list = os.walk(self.path, topdown=False)
        except OSError as e:
            err = e.errno
            pass
        if err == 0:
            seq = list()
            for root, dirs, files in file_list:
                for name in files:
                    f_path = os.path.join(root, name)
                    os.stat_float_times(True)
                    file_stats = os.stat(f_path)
                    f_time = file_stats.st_birthtime
                    f_size = file_stats.st_size
                    f = os.path.basename(f_path)

                    not (f.startswith('.') or f.endswith('\r')) and seq.append({
                        'filename': f,
                        'path': f_path,
                        'time': f_time,
                        'size': f_size
                    })

            sorted_file_list = sorted(seq, key=lambda k: k['time'], reverse=reverse)
            return sorted_file_list

    @staticmethod
    def convertFileSize(size_bytes):
        """
        Convert filesize in bytes
        :param size_bytes: float()
        :return: formatted file size: str()
        """
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "{0} {1}".format(s, size_name[i])

    @staticmethod
    def search(query, dict_list):
        """
        Search string in a list of Dict
        :param query: str()
        :param dict_list: list(dict())
        :return: list(dict())
        """
        seq = list()
        for d in dict_list:
            if d['filename'].lower().startswith(query.lower()):
                seq.append(d)
        return seq


def parseWorkingDir(directory):
    """
    Parse working directory and adjust if not absolute
    :param directory:
    :return: path str()
    """
    path = str(directory).replace(':', '/')
    if not (str(path).startswith('/')):
        u_dir = os.path.expanduser('~')
        path = "{0}/{1}".format(u_dir, path)
    return path


t_dir = Tools.getEnv('directory')
search_subfolders = True if Tools.getEnv('search_subfolders') == "True" else False
working_path = parseWorkingDir(t_dir)
query = Tools.getArgv(1)
date_format = Tools.getEnv('date_format')


files_in_directory = None
file_list = list()
if working_path:
    rf = RecentFiles(working_path)
    files_in_directory = rf.getRecentFilesDeep(reverse=True) if search_subfolders else rf.getRecentFiles(reverse=True)
    file_list = RecentFiles.search(query, files_in_directory) if bool(
        query) and files_in_directory else files_in_directory

wf = Items()

# When path not found, expose error to script filter
if files_in_directory is None:
    wf.setItem(
        title='Path "{0}" not found...'.format(t_dir),
        subtitle='Change path in List Filter, e.g. /Users/<user>/Desktop',
        valid=False
    )
    wf.setIcon('attention.png', 'png')
    wf.addItem()
# In case no files were found in directory
elif len(files_in_directory) == 0:
    wf.setItem(
        title='Folder is empty!',
        subtitle="ENTER to start again",
        arg="*RESTART*",
        valid=True
    )
    wf.setIcon('attention.png', 'png')
    wf.addItem()
# if file search has no results
elif len(file_list) == 0:
    wf.setItem(
        title='Cannot find file starting with "{0}"'.format(query),
        valid=False
    )
    wf.setIcon('attention.png', 'png')
    wf.addItem()
# Expose sorted file list to Script Filter
else:
    for d in file_list:
        path = d['path']
        size = RecentFiles.convertFileSize(
            d['size']) if os.path.isfile(path) else '-'
        filename = d['filename']
        a_date = Tools.getDateStr(d['time'], date_format)

        wf.setItem(
            title=filename,
            type='file',
            subtitle='Added: {0}, Size: {1}'.format(
                a_date, size),
            arg=path,
            quicklookurl=path
        )
        wf.setIcon(path, 'fileicon')
        wf.addItem()
wf.write()
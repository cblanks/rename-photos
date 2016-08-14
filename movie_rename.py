#!/usr/bin/python

"""
Rename movies in target directory with date taken.
"""

import subprocess as sp
from json import loads
from os import getcwd, listdir, rename, stat
from os.path import isdir, isfile
from sys import argv
from datetime import datetime

try:
    movie_dir = argv[1]
except IndexError:
    movie_dir = getcwd()

for m in listdir(movie_dir):

    ext = m.split('.')[-1].lower()
    if not ext in ['3gp', 'mp4', 'mpeg', 'mpg', 'mov']:
        continue
        
    m_path = '%s\\%s' % (movie_dir, m)
    if isdir(m_path):
        continue
        
    cmd = [
        'ffprobe', '-v', 'quiet',
        '-show_format', '-print_format', 'json',
        m_path.replace(' ', ' ')
    ]

    proc = sp.Popen(cmd, stdout=sp.PIPE)
    
    try:
        tag = proc.stdout.read().decode(encoding='UTF-8')
        meta = loads(tag)
        date_shot = meta['format']['tags']['creation_time']
        print(meta['format'].keys())
    except:
        date_shot = None
                
    if date_shot is None:
        if not 'n'==input('META datetime not found for %s.  Use file creation datetime? [Y]/n ' % m):
            date_shot = datetime.utcfromtimestamp(stat(m_path).st_birthtime).isoformat()
            date_shot = date_shot.replace('T', ' ')
            date_shot = date_shot.replace('-', ':')
            
        else:
            continue
    
    date_str = date_shot.split(' ')[0]
    date_str = date_str.replace(':', '-')
    
    time_str = date_shot.split(' ')[1]
    time_str = time_str.replace(':', '.')

    i = 0
    target_path = '%s/%s %s.%s' % (movie_dir, date_str, time_str, ext)
    
    while isfile(target_path) is True and target_path != m_path:
        i += 1
        target_path = '%s/%s %s %i.%s' % (movie_dir, date_str, time_str, i, ext)
        
    if target_path != m_path:
        rename(m_path, target_path)

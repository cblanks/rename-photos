#!/usr/bin/python

"""
View movie metadata.
"""

import subprocess as sp
from sys import argv
from json import load, loads

movie_path = argv[1]

tag = sp.Popen([
    'ffprobe', '-v', 'quiet', '-show_format', '-print_format', 'json',
    movie_path
], stdout=sp.PIPE)

sout = tag.stdout.read().decode(encoding='UTF-8')
meta = loads(sout)

print(meta['format']['tags']['creation_time'])


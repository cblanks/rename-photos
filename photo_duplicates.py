#!/usr/bin/python

"""
Show photos taken in the same second.
"""
from os import getcwd, listdir, system
from sys import argv

try:
    photo_dir = argv[1]
except IndexError:
    photo_dir = getcwd()

try:
    max_count = argv[2]
except IndexError:
    max_count = 10

count = 0
for p in listdir(photo_dir):

    if p[0] == '.':
        continue
    
    p_path = (photo_dir+'/'+p).replace('//', '/')
    
    if p_path.find('_01.') > -1:
        system("open %r*" % (p_path.split('.')[0] + '.').replace('_01.', ''))
        
        count += 1
        if count>max_count:
            print 'more remaining.  please run again'
            break

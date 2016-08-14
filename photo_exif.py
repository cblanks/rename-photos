#!/usr/bin/python

"""
View photo metadata.
"""

from exifread import process_file
from sys import argv

photo_path = argv[1]
    
with open(photo_path, 'rb') as f:
    tag = process_file(f)
    
    for k in tag.keys():
        if k.lower().find('date')>-1:
            print(k, ':', tag[k])
        print(k)

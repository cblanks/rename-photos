#!/usr/bin/python

#  d o c s t r i n g s
"""
Rename photos in target directory with date taken.
Christopher BLANKS
2015-08-14
"""

#  d e p e n d e n c i e s
import exifread, os, sys
from datetime import datetime

#  c l a s s e s
class Photo():

    # internal
    def __init__(self, file_path):
        self.__file_path__ = file_path
        self.__ext__ = '.' + self.__file_path__.split('.')[-1].lower()
        self.__date__ = self.__findDate__()
        print(self.__date__)
        
    def __findDate__(self):
        dates = {}
        exif_format = '%Y:%m:%d %H:%M:%S' #2015:07:02 10:54:09
        
        # load EXIF data
        with open(self.__file_path__, 'rb') as f:
            try:
                tag = exifread.process_file(f)
                for k in tag.keys():
                    if -1 < k.lower().find('date'):
                        dates[k] = datetime.strptime(tag[k].printable, exif_format)
            except:
                pass
            
        # if no EXIF data, load file created date
        if 0 == len(dates.keys()):
            dates['ctime'] = datetime.fromtimestamp(os.path.getctime(self.__file_path__))

        # take the oldest of all dates found to be the creation date
        try:
            return sorted(dates.values())[0]
        except IndexError:
            return None
        
    def __getDirName__(self):
        return os.path.dirname(self.__file_path__)
        
    # external
    def getOriginalName(self):
        return os.path.basename(self.__file_path__)[:-1*len(self.__ext__)]
         
    def getTargetName(self):
        if None == self.__date__:
            return self.getOriginalName
        else:
            return datetime.strftime(
                self.__date__, 
                '%Y-%m-%d %H.%M.%S' #2015-07-02 10.54.09
                #'%Y-%m-%d %H.%M.%S.%f' #2015-07-02 10.54.09.000001
            )
    
    def getDate(self):
        return self.__date__

    def getOriginalPath(self):
        return self.__file_path__

    def getTempPath(self):
        return '%s\\_%s%s' % (self.__getDirName__(), self.getOriginalName(), self.__ext__)
        
    def getTargetPath(self, i=0):
        t = '%s/%s' % (self.__getDirName__(), self.getTargetName())
        if 0 < i:
            t += ' %i' % i

        return t + self.__ext__

#  f u n c t i o n s
def __listPhotos__(path, ext=['jpg', 'jpeg', 'png']):
    photos = []
    for root, dirs, files in os.walk(photo_dir):
        for f in files:
            # skip if not an image
            if not f.split('.')[-1].lower() in ['jpg', 'jpeg', 'png']:
                continue
            
            photos.append(Photo(os.path.join(root, f)))

    return photos

def __sortPhotos__(photos=[]):
    return photos

#  v a r i a b l e s
try:
    photo_dir = sys.argv[1]
except IndexError:
    photo_dir = os.getcwd()

photo_dir = os.path.abspath(photo_dir)

#  m a i n
photos = __listPhotos__(photo_dir)
for P in photos:
    
    # skip if already name will not change 
    if P.getTargetName() == P.getOriginalName():
        continue
        
    # list other photos named by same date
    contemporary = []
    for Q in photos:
        if P.getDate() == Q.getDate():
            contemporary.append(Q)
    
    # rename photo(s)
    for C in contemporary:
        #print(C.getOriginalPath(), C.getTempPath())
        os.rename(C.getOriginalPath(), C.getTempPath())
        
    s = __sortPhotos__(contemporary)
    for i in range(len(s)):
        os.rename(s[i].getTempPath(), s[i].getTargetPath(i))
        

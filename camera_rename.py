#!/usr/bin/python

#  d o c s t r i n g s
"""
Rename photos and videos in target directory with date taken.
Christopher BLANKS
2015-08-16
"""

#  d e p e n d e n c i e s
import exifread, json, os, subprocess, sys
from datetime import datetime

#  c l a s s e s
class Camera():
    """
    Base class for photos and videos taken from a camera.
    """
    # variables
    date_format = '%Y-%m-%d %H.%M.%S' #2015-07-02 10.54.09
    
    # internal
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__ext = '.' + self.__file_path.split('.')[-1].lower()
        self.__date = None

    def __getDate(self):
        self.__date = self.__date or self.__findDate()
        return self.__date
        
    def __getDirName(self):
        return os.path.dirname(self.__file_path)
        
    def __findMetaDate(self):
        return []
        
    def __findDate(self):
        dates = [
            datetime.fromtimestamp(os.path.getatime(self.__file_path)),
            datetime.fromtimestamp(os.path.getctime(self.__file_path)),
            datetime.fromtimestamp(os.path.getmtime(self.__file_path))
        ]
        
        dates.extend(self.__findMetaDate())
        
        try:
            return sorted(dates)[0]
        
        except IndexError:
            return None
        
    def __getOriginalName(self):
        return os.path.basename(self.__file_path)[:-1*len(self.__ext)]
        
    def __getTargetName(self):
        if None == self.__getDate():
            return self.__getOriginalName()
        else:
            return datetime.strftime(
                self.__getDate(), 
                self.date_format
            )
    
    # external
    def isWellNamed(self):
        return self.__getTargetName() == self.__getOriginalName()
        
    def getOriginalPath(self):
        return self.__file_path

    def getTargetPath(self, i=0):
        t = '%s/%s' % (self.__getDirName(), self.__getTargetName())
        if 0 < i:
            t += ' %i' % i
            
        return t + self.__ext


class Photo(Camera):

    # internal
    def _Camera__findMetaDate(self):

        exif_format = '%Y:%m:%d %H:%M:%S' #2015:07:02 10:54:09

        dates = []
        with open(self._Camera__file_path, 'rb') as f:
            try:
                tag = exifread.process_file(f)
                for k in tag.keys():
                    if -1 < k.lower().find('date'):
                        dates.append(datetime.strptime(tag[k].printable, exif_format))
            except:
                pass
                
        return dates

class Movie(Camera):

    # internal
    def _Camera__findMetaDate(self):
        
        meta_format = '%Y-%m-%d %H:%M:%S' #2015-07-02 10:54:09
        
        cmd = [
            'ffprobe', '-v', 'quiet',
            '-show_format', '-print_format', 'json',
            self._Camera__file_path.replace(' ', ' ')
        ]
        
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        
        try:
            tag = proc.stdout.read().decode(encoding='UTF-8')
            metadata = json.loads(tag)
            return [datetime.strptime(metadata['format']['tags']['creation_time'], meta_format)]
            
        except:
            return []
        

#  f u n c t i o n s
def __list(my_dir, exts=[]):
    my_exts = []
    for e in exts:
        my_exts.append(e.lower())
        
    my_list = []
    for a in os.listdir(my_dir):
        
        a_path = os.path.join(my_dir, a)
        
        if not os.path.isfile(a_path):
            continue
            
        if not a.split('.')[-1].lower() in my_exts:
            continue
            
        my_list.append(a_path)
        
    return my_list

def __listPhotos(my_dir, my_exts=['jpg', 'jpeg', 'png']):
    photos = []
    for p in __list(my_dir, my_exts):
        photos.append(Photo(p))
        
    return photos

def __listMovies(my_dir, my_exts=['3gp', 'mp4', 'mpg', 'mpeg', 'mov', 'avi']):
    movies = []
    for m in __list(my_dir, my_exts):
        movies.append(Movie(m))
        
    return movies


#  v a r i a b l e s
try:
    camera_dir = sys.argv[1]
except IndexError:
    camera_dir = os.getcwd()

camera_dir = os.path.abspath(camera_dir)


#  m a i n
movies = __listMovies(camera_dir)
photos = __listPhotos(camera_dir)

for A in photos+movies:
    
    if A.isWellNamed():
        continue

    i = 0
    while i<100:
        target_path = A.getTargetPath(i)
        
        if os.path.isfile(target_path):
            i += 1
        else:
            os.rename(A.getOriginalPath(), target_path)
            break

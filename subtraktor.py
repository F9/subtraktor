#!/usr/bin/env python
"""Subtraktor v1.0 beta by Gavoja moded by F9.
    F9 Website: http://www.9lli.it/francesco
    Powered by www.OpenSubtitles.org (http://www.opensubtitles.org).
    """

import os, glob
import sys
import struct
import xmlrpclib
import base64
import gzip
import StringIO
from time import sleep
from os import listdir

HOST = "http://api.opensubtitles.org/xml-rpc"
USER = "" #PUT YOUR USERNAME
PASSWORD = "" #PUT YUOUR PASSWORD
AGENT = "OS Test User Agent"
EXTENSIONS = [".avi", ".mp4", ".mpg", ".mpeg"]
DEFAULT_LANGUAGE = "ita" #PUT YOUR LANGUAGE
INDEX = 0
MYPATH = "/media/USBHD/pyDownload/" #PUT YOUR DOWNLOAD DIR

class Subtraktor(object):
    def __init__(self):
        pass
    
    def connect(self):
        self._get_language()
        self.service = xmlrpclib.ServerProxy(HOST)
        self.token = self._get_token()
    
    def _get_language(self):
        self.language = DEFAULT_LANGUAGE
    
    def _get_token(self):
        result = self.service.LogIn(USER, PASSWORD, self.language, AGENT)
        
        if not result.has_key("token"):
            raise Exception, "Unable to log in."
        return result["token"]
    
    def _get_move_hash(self, path):
        try:
            longlongformat = 'q'  # long long
            bytesize = struct.calcsize(longlongformat)
            
            f = open(path, "rb")
            
            filesize = os.path.getsize(path)
            hash = filesize
            
            if filesize < 65536 * 2:
                return "SizeError"
            
            for x in range(65536/bytesize):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number
            
            f.seek(max(0,filesize-65536),0)
            for x in range(65536/bytesize):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF
            
            f.close()
            returnedhash =  "%016x" % hash
            return returnedhash
        
        except(IOError):
            return "IOError"
    
    def _get_move_size(self, path):
        result = os.stat(path)
        return result.st_size
    
    def _get_subtitle_id(self, movie_hash, movie_size):
        arg = [{
               "sublanguageid": self.language,
               "moviehash":movie_hash,
               "moviebytesize":movie_size}]
        result = self.service.SearchSubtitles(self.token, arg)
        
        if result["data"]:
            return result["data"][INDEX]["IDSubtitleFile"]
        return None
    
    def _get_subtitle_data(self, subtitle_id):
        result = self.service.DownloadSubtitles(self.token, [subtitle_id])
        content = result["data"][0]["data"]
        content = base64.b64decode(content)
        stream = StringIO.StringIO(content)
        f = gzip.GzipFile(fileobj=stream)
        data = f.read()
        return data
    
    def _save_subtitle(self, path, data):
        base, extension = os.path.splitext(path)
        sub_path = "{0}.txt".format(base)
        
        with open(sub_path, "w") as f:
            f.write(data)
    
    def _get_movie_title(self, path):
        return os.path.split(movie)[1]
    
    def download(self, path):
        movie_hash = self._get_move_hash(path)
        movie_size = self._get_move_size(path)
        subtitle_id = self._get_subtitle_id(movie_hash, movie_size)
        
        if not subtitle_id:
            return "  Subtitles not found.",subtitle_id,movie_hash
        
        data = self._get_subtitle_data(subtitle_id)
        self._save_subtitle(path, data)
        return "  OK."
    
    def _message(self, text):
        pass

def is_movie(path):
    name, ext = os.path.splitext(path)
    print path
    if not ext in EXTENSIONS:
        return False
    return True

def list_folder(path):
    movies = []
    for path, subdirs, files in os.walk(path):
    	for name in files:
        	if(is_movie(os.path.join(path, name))):
                movies.append(os.path.join(path, name))
    
    return movies

def main():
    print __doc__
    
    
    movies = []
    movies =  list_folder(MYPATH)
    
    try:
        # Initialize Subtraktor class.
        p = Subtraktor()
        p.connect()
        
        # Download subs for all selected movies.
        for m in movies:
            print "Movie: {0}".format(os.path.basename(m))
            print p.download(m)
        sleep(1)
    except Exception, e:
        print "Error: {0}".format(e.strerror)



if __name__ == '__main__':
    main()

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
USER = "iF9"
PASSWORD = "892892"
AGENT = "OS Test User Agent"
EXTENSIONS = [".avi", ".mp4", ".mpg", ".mpeg"]
DEFAULT_LANGUAGE = "ita"
INDEX = 0
MYPATH = "/media/USBHD/pyDownload/"

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


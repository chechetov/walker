#! /usr/bin/python3

import os
import glob
import re
from time import sleep

TARGET_PATH = '/var/lib/vz/private/Projects/'
res = []


with open('files.txt','w') as filelist:
     for root, dirs, files in os.walk(TARGET_PATH):
          for file in files:
               if file.endswith('.msi') and int(os.stat(os.path.join(root,file)).st_mtime) > 1451606400:
                   #print("{0}".format(os.path.join(root,file), os.stat(os.path.join(root,file)).st_mtime))
                   filelist.write("{0} \n".format(os.path.join(root,file)))


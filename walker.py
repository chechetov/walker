#! /usr/bin/python3

import os
import glob
import re
from time import sleep

# This script creates a list of msi files, which:
# Reside in target path
# Are created after target timestamp
# Exports to 'files.txt' in the working directory


TARGET_PATH = '/var/lib/vz/private/Projects/'
TARGET_TIMESTAMP = 1451606400
res = []


with open('files.txt','w') as filelist:
     for root, dirs, files in os.walk(TARGET_PATH):
          for file in files:
               if file.endswith('.msi') and int(os.stat(os.path.join(root,file)).st_mtime) > TARGET_TIMESTAMP:
                   #print("{0}".format(os.path.join(root,file), os.stat(os.path.join(root,file)).st_mtime))
                   filelist.write("{0} \n".format(os.path.join(root,file)))


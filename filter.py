
#! /usr/bin/python3

import os

words = ['#sources','#source','#Sources','#Source','Source','Sources','source','sources']

with open('files.txt','r') as files:
     clearlist = [file for file in files if all(dir not in words for dir in os.path.dirname(file).split('/'))]

print(len(clearlist))

with open('filtered.txt','w') as filtered:
     for filepath in clearlist:     
         filtered.write(filepath)


         

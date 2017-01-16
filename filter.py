
#! /usr/bin/python3

import os


# This tiny thing gets 'files.txt' in the working dir as input
# and filters them according to this rule: 
# if any element in full path of file contains word from 'words' array - file is excluded

# Exports result to 'filtered.txt'


words = ['#sources','#source','#Sources','#Source','Source','Sources','source','sources']

with open('files.txt','r') as files:
     clearlist = [file for file in files if all(dir not in words for dir in os.path.dirname(file).split('/'))]

print(len(clearlist))

with open('filtered.txt','w') as filtered:
     for filepath in clearlist:     
         filtered.write(filepath)


         

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import sys
import shutil

def touch(arg1,arg2,arg3):
    arg1 = ('file://{}'.format(arg1))
    html_page = urllib2.urlopen(arg1).read()
    soup = BeautifulSoup(html_page)

    for item in soup.findAll("div", {"class": "body"}):
        try:
            name = item.find('div', {"class": "text"}).text
            #img = item.find("img", {"class": "photo"})['src']
            img = item.find("a", {"class": "photo_wrap clearfix pull_left"})['href']
            img = img.split('/')[-1]
            source = ('{}{}'.format(arg2,img))
            destination = ('{}{}'.format(arg3,name))

            shutil.copy2(source, destination)
            print(source, destination)

        except:
            pass

if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
    except:
        print ("Example usage: ./parse.py /path/to/source/file.html /path/to/images/ /path/to/destination/")
        sys.exit(1)

    touch(arg1,arg2,arg3)

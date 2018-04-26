#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import sys

def touch(argv):
	z = argv
	html_page = urllib2.urlopen(argv)
	soup = BeautifulSoup(html_page)
	for link in soup.findAll('a'):
        print z+link.get('href')

if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
    except:
        print ("Example usage: ./hrefparse.py http://example.com")
        sys.exit(1)

    # start the program
    touch(arg1)

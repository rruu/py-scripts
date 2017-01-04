#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import sys
import os
from lxml import html

def touch(argv):

    a,b,c,d,e,f = argv.split('/')
    z = f.strip('.html')
    if not os.path.exists(z):
        os.makedirs(z)
    os.chdir(z)
    page = requests.get(argv)
    webpage = html.fromstring(page.content)
    links = webpage.xpath('//figcaption[@class="file-attr"]/a/@href')
    with open (z+".txt", "w") as linkf:
        for link in links:
            if 'jpg' not in link and 'png' not in link:
                linkf.write(str('https://2ch.hk/b/'+link[3:]) +"\n")

    os.system('wget -nc -i' +z+".txt")

if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
    except:
        print ("Example usage: ./webm.py https://2ch.hk/b/res/143523622.html")
        sys.exit(1)

    # start the program
    touch(arg1)

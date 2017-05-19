#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# users.txt url line by line
# https://vk.com/id50024638
# https://vk.com/kerribel
# https://vk.com/id54982838
# https://vk.com/svirido4ka

import sys
import requests
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock
import urllib.request, urllib.error

url = [line.strip() for line in open("users.txt", 'r')]

def parse(url):
    try:
        url1 = "http://showid.ru/names/"+url
        page = requests.get(url1)
        tree = html.fromstring(page.content)
        brodcasts = tree.xpath('//div[@class="row"]/div[@class="col-xs-12 col-md-6 col-lg-5 item_info"]/p[2]/text()')
        print(str(brodcasts)[3:-2],";",url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return
        else:
            return
    except:
        return

lock = Lock()
pool = ThreadPool(5)

pool.map(parse, url)
pool.close()
pool.join()

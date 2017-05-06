#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import html
import requests
from pyperi import Peri
import urllib.request, urllib.error
import sys#, socks, socket
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock

pp = Peri()

#socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
#socket.socket = socks.socksocket

orig_stdout = sys.stdout
f = open('parse-omg.txt', 'a')
sys.stdout = f

url = ['http://liveomg.com/?lang=ru&next=1', 'http://liveomg.com/?lang=ru&next=101', 'http://liveomg.com/?lang=ru&next=201', 'http://liveomg.com/?lang=ru&next=301', 'http://liveomg.com/?lang=ru&next=401']
brodcasts_url = "periscope.tv/w/"

def parse(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    brodcasts = tree.xpath('//a[@class="username"]/@href')
    for i in brodcasts:
        try:
            x = pp.get_broadcast_info(i[-13:])
            print(brodcasts_url+x['id'], "uid:", x['user_id'], "username:", x['username'], "\tname:",x['user_display_name'],"\ttitle:", x['status'])
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return
            else:
                return
        except:
            return

    sys.stdout = orig_stdout
    f.close()

lock = Lock()
pool = ThreadPool(5)

pool.map(parse, url)
pool.close()
pool.join()

# -*- coding: utf-8 -*-

import sys
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock
import urllib.request, urllib.error
from datetime import datetime
import socket

socket.setdefaulttimeout(20)

urls = [line.strip() for line in open(sys.argv[1], 'r')]

def parse(urls):
    try:
        url = str(urls[7:-1])
        login = url.split(':')[0]
        passw = url.split(':')[1]
        passw = passw.split('@')[0]
        snappath = url.split('@')[1]
        dtnow = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = snappath.split(':')[0]
        filename = str(filename + "-" + dtnow + ".jpg")
        #print(url)
        urllib.request.urlretrieve("http://" + str(snappath) + "/snapshot.cgi?user=" + str(login) + "&pwd=" + str(passw), filename)

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(str(snappath) + " err ")
        else:
            print(str(snappath) + " err ")
    except:
        print(str(snappath) + " err ")

lock = Lock()
pool = ThreadPool(20)

pool.map(parse, urls)
pool.close()
pool.join()

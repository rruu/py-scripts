# -*- coding: utf-8 -*-
import requests as req
import sys
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock
import urllib.request, urllib.error


ip = [line.strip() for line in open(sys.argv[1], 'r')]
port = sys.argv[2]

def parse(ip):
    try:
        resp = req.head("http://" + str(ip) + ":" + str(port), verify=False, timeout=3)
        print(str(ip) + "," + str(port) + "," + resp.headers['server'])
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return
        else:
            return
    except:
        return

lock = Lock()
pool = ThreadPool(20)

pool.map(parse, ip)
pool.close()
pool.join()

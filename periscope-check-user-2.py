#!/usr/bin/python3
#coding: utf-8
import urllib.request, urllib.error
import sys, csv, time
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock

if len(sys.argv) != 2:
    print("Usage: %s /path/to/users.csv" % (str(sys.argv[0])))
    sys.exit(1)

filecsv_file = sys.argv[1]

PERISCOPE_URL = 'https://www.periscope.tv/'
#usernames = []

def attempt(unames):
    try:
        conn = urllib.request.urlopen(PERISCOPE_URL+unames[:-2])
    except urllib.error.HTTPError as e:
        if e.code == 408:
            return
        else:
            pass
        print("[ + ] " + str(e.code) + " " + unames[:-2])
    else:
        print("[ - ] "+ str(conn.getcode()) + " " + unames[:-2])

with open(filecsv_file, "r") as f:
    reader = csv.reader(f, delimiter=',')
    usernames2 = list(reader)
    unames = usernames2[0]
lock = Lock()
pool = ThreadPool(10)

pool.map(attempt, unames)
pool.close()
pool.join()

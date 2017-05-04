#!/usr/bin/python3
#coding: utf-8
# pyperi https://github.com/takeontom/PyPeri
from pyperi import Peri
import urllib.request, urllib.error
import sys, csv, time
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock

pp = Peri()

if len(sys.argv) != 2:
    print("Usage: %s /path/to/users.csv" % (str(sys.argv[0])))
    sys.exit(1)

filecsv_file = sys.argv[1]

usernames = []

def attempt(unames):
    try:
        conn = pp.request_api('getUserPublic', username=unames[:-2])
        print(" ID:", conn['user']['id'], " Followers: ", conn['user']['n_followers'], " \tUsersname: " ,conn['user']['username'])
    except:
        #print(e.code)
        return

with open(filecsv_file, "r") as f:
    reader = csv.reader(f, delimiter=',')
    usernames2 = list(reader)
    unames = usernames2[0]
lock = Lock()
pool = ThreadPool(5)

pool.map(attempt, unames)
pool.close()
pool.join()

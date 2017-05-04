#!/usr/bin/python3
#coding: utf-8
# pyperi https://github.com/takeontom/PyPeri
import json
import urllib.request, urllib.error
import sys, csv, time
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock

if len(sys.argv) != 2:
    print("Usage: %s /path/to/users.csv" % (str(sys.argv[0])))
    sys.exit(1)

filecsv_file = sys.argv[1]

usernames = []
emb = "https://embed.pscp.tv/user/"

def attempt(unames):
    try:
        response = urllib.request.urlopen(emb+unames[:-2]+".json")
        print("Username: ",unames[:-2]," \t Broadcast RUN: ",json.loads(response.read().decode('utf-8'))['broadcast_id'])

    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("Username: ", unames[:-2], "\t - Not found")
        else:
            return
    except:
        #print(e.code)
        print("Username: ", unames[:-2], "\t Not running")
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

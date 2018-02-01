# -*- coding: utf-8 -*-
import socket
import sys
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock

name = [line.strip() for line in open(sys.argv[1], 'r')]

def parse(name):
    try:
        print(str(name) + " : " + socket.gethostbyname(str(name)))
    except socket.error:
        return
    except:
        return

lock = Lock()
pool = ThreadPool(20)

pool.map(parse, name)
pool.close()
pool.join()

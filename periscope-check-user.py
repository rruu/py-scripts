#!/usr/bin/python3
#coding: utf-8
import urllib.request, urllib.error
import sys, csv

PERISCOPE_URL = 'https://www.periscope.tv/'

with open('users.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    usernames2 = list(reader)
usernames = usernames2[0]

for uname in usernames:
    try:
        conn = urllib.request.urlopen(PERISCOPE_URL+uname[:-2])
    except urllib.error.HTTPError as e:
        code1=(e.code)
    else:
        print(uname[:-2])

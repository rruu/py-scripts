#!/usr/bin/python3
#coding: utf-8

import socket
import socks
import urllib.request as ur

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

s = ur.urlopen("https://ifconfig.co")
sl = s.read()
print(sl)

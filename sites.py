#!/usr/bin/env python3
import sys
import lxml.etree
import lxml.html
import requests
import ipaddress

user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Usage: %s 127.0.0.1/24 (cidr)" % (str(sys.argv[0])))
    sys.exit(1)

input_ips = sys.argv[1]
ips = ipaddress.ip_network(input_ips, False)

def getsites(ip):
    r = requests.get("https://ipinfo.io/{}".format(ip), headers = user_agent)
    root = lxml.html.fromstring(r.content)
    sites = root.xpath('//tr/td/text()')[10:]
    for s in sites:
        print('{}'.format(s))

for ip in ips: getsites(ip)

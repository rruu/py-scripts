#!/usr/bin/env python3
import cursor
import lxml.etree
import lxml.html
import requests
import sys

cursor.hide()

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Usage: %s AS (AS24940)" % (str(sys.argv[0])))
    sys.exit(1)

code = sys.argv[1]

try:
    r = requests.get("https://ipinfo.io/{}".format(code))
    #print("https://ipinfo.io/{}".format(code))
    r1 = lxml.html.fromstring(r.content)
    addrss = r1.xpath('//div[@id="ipv4-data"]/table[@id="block-table"]/tbody[@class="t-14"]/tr/td[1]/a')
    for z in addrss:
        print("{}".format((z.text).strip()))
except:
    print('err')

cursor.show()

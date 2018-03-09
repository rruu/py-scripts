#!/usr/bin/env python3
import lxml.etree
import lxml.html
import requests
import sys

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Usage: %s RU (country code)" % (str(sys.argv[0])))
    sys.exit(1)

code = sys.argv[1]

try:
    r = requests.get("https://ipinfo.io/countries/{}".format(code))
    root = lxml.html.fromstring(r.content)
    aslist = root.xpath('//tr/td[1]/a')
    print("https://ipinfo.io/countries/{}".format(code))   
    for asn in aslist:
        r2 = requests.get("http://ipinfo.io/{}".format(asn.text))
        #print("http://ipinfo.io/{}".format(asn.text))
        r3 = lxml.html.fromstring(r2.content)
        print("Get ip from: {}\r".format(asn.text), end="\r")
        f = open("{}.log".format(code),'a')
        addrss = r3.xpath('//div[@id="ipv4-data"]/table[@id="block-table"]/tbody[@class="t-14"]/tr/td[1]/a')
        for z in addrss:
            f.write("{}\n".format(z.text))
            #print(z.text)
except:
    print("err")
f.close()

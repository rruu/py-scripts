#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import sys
import os
from lxml import html
ur1 = "https://www.expireddomains.net/backorder-expired-domains/?start="
ur2 = "&ftlds[]=595"

n = 0
# rang of count pages for parse
for r in range(100):
    #print(n)
    z = str(ur1)+str(n)+str(ur2)
    page = requests.get(z)
    webpage = html.fromstring(page.content)
    domains = webpage.xpath('//td[@class="field_domain"]//text()')
    n += 25
    for domain in domains:
        print(domain)

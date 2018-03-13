#!/usr/bin/env python3
import os
import lxml.etree
import lxml.html

htmlfile = '/print/index.html'
rootdir = '/root/finmag2/'

#f = open("/root/finmag/335/print/index.html", encoding ='windows-1251')
#[x for x in body if 'доступа к полной версии' in x]

# 4653  - Платных
# 174   - Нету print
# 9293  - Больше 500 знаков

for i in os.listdir(rootdir):
    try:
        f = open("{}{}{}".format(rootdir,i,htmlfile), encoding ='windows-1251')
        page = f.read()
        tree = lxml.html.fromstring(page)
        #print("{}{}{}".format(rootdir,i,htmlfile))
 
        title = tree.xpath('//html/body/table/tr/td/h3/text()')
        if title == []:
            title = tree.xpath('//html/body/table/tr/td/div/h3/text()')
            if title == []:
                title = tree.xpath('//html/body/table/tr/td/p[3]/text()')

        body = tree.xpath('//body/table/tr/td/table/tr//text()')
#        body = ''.join(map(str, body))
#        body = body.strip().rstrip('\n')
        if [x for x in body if 'полной версии' in x] != []:
            #print("{}{}{} \t - Платная".format(rootdir,i,htmlfile))
            pass
        if body == []:
            body = tree.xpath('//body//tr/td/div//text()')[4:]
            if [x for x in body if 'полной версии' in x] != []:
                #print("{}{}{} \t - Платная".format(rootdir,i,htmlfile))
                pass

        body = ''.join(map(str, body))
        body = body.strip().rstrip('\n')
        img = tree.xpath('//td/img/@src')

        if len(body) > 500:
            #print("{}{}{} \t - Знаков : {} - Title: {} \t - IMG: {}".format(rootdir,i,htmlfile,len(body),title,img))
            print("{}")

    except IOError:
        #print("{}{}{} \t - Не найдено".format(rootdir,i,htmlfile))
        pass




#!/usr/bin/env python3
import os
import lxml.etree
import lxml.html
htmlfile = '/print/index.html'
rootdir = '/root/tmp/fin/'
newpath = '/root/new/'
imgpath = '/root/tmp/finansmag_ru/i/'
copyright = '\n\nЖурнал «Финанс.» '

os.system('wp term create category Финанс --description="Журнал Финанс" --allow-root --path=/var/www/html')

for i in os.listdir(rootdir):
    try:
        f = open("{}{}{}".format(rootdir,i,htmlfile), encoding ='windows-1251')
        #print("{}{}{}".format(rootdir,i,htmlfile))
        page = f.read()
        tree = lxml.html.fromstring(page)
        #print("{}{}{}".format(rootdir,i,htmlfile))
 
        title = tree.xpath('//html/body/table/tr/td/h3/text()')
        if title == []:
            title = tree.xpath('//html/body/table/tr/td/div/h3/text()')
            if title == []:
                title = tree.xpath('//html/body/table/tr/td/p[3]/text()')

        body = tree.xpath('//body/table/tr/td/table/tr//text()')
        if [x for x in body if 'полной версии' in x] != []:
            #print("{}{}{} \t - Платная".format(rootdir,i,htmlfile))
            pass
        if body == []:
            body = tree.xpath('//body//tr/td/div//text()')[4:]
            if [x for x in body if 'полной версии' in x] != []:
                #print("{}{}{} \t - Платная".format(rootdir,i,htmlfile))
                pass

        if tree.xpath('//tr/td/p/text()') == []:
            try:
                subtitle = tree.xpath('//tr/td/div/p/text()')[0]
                if len(tree.xpath('//tr/td/div/p/text()')[1]) < 50 and tree.xpath('//tr/td/div/p/text()')[1] != []:
                    author = tree.xpath('//tr/td/div/p/text()')[1]
                else:
                    author = ''
            except IndexError:
                author = ''

        else:
            try:
                subtitle = tree.xpath('//tr/td/p/text()')[0]
                if len(tree.xpath('//tr/td/p/text()')[1]) < 50 and tree.xpath('//tr/td/p/text()')[1] != []:
                    author = tree.xpath('//tr/td/p/text()')[1]
                else:
                    author = ''
            except IndexError:
                author = ''


        body = ''.join(map(str, body))
        body = body.strip().rstrip('\n')
        body = "\n\n".join(body.split("\n"))

        img = tree.xpath('//td/img/@src')
        img = str(img).split('/')[-4:]
        title = title[0]

        if len(body) > 500 and 'полной версии' not in body:
            f = open("/root/out/{}".format(i),"w")
            f.write(body)
            f.close()
            f = open("/root/out/{}".format(i),"a")
            f.write(copyright+subtitle+"\n "+author)
            f.close()

        if len(body) < 500:
            pass

        if img == ['[]']:
            if os.path.isfile("/root/out/{}".format(i)):
                comms1 = "wp post create /root/out/{} --post_title='{}' --post_status=publish --allow-root --path=/var/www/html/ --post_category='Финанс'".format(i,title)
                print("Article (without img): {} - added".format(i))
                os.system(comms1)
            else:
                pass
        else:
            img = (imgpath + "/" + img[-3]+ "/" + img[-2]+ "/" + img[-1][:-2])

            comms2 = ("wp media import {} --post_id=$(wp post create /root/out/{} --post_title='{}' --post_status=publish --porcelain --allow-root --path=/var/www/html/ --post_category='Финанс') --featured_image --allow-root --path=/var/www/html/ \n".format(img,i,title))
            os.system(comms2)
            print("Article (with img): {} - added".format(i))

    except IOError:
        pass

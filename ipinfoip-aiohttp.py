#!/usr/bin/env python3
import lxml.html
import asyncio, aiohttp, sys

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Usage: %s RU (country code)" % (str(sys.argv[0])))
    sys.exit(1)

code = sys.argv[1]

source = ["https://ipinfo.io/countries/{}".format(code)]
urls = []
result = []

#async def fetch(session, url, ssl=ssl.SSLContext()):
async def fetch(session, url):
    async with session.get(url) as response:
        print("{} - \t {}".format(url,response.status), end='\r')
        return await response.text()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results


if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    s = loop.run_until_complete(fetch_all(source, loop))
    for u in s:
        u = lxml.html.fromstring(u)
        u = u.xpath('//tr/td[1]/a')
        for z in u:
            #print(z.text)
            urls.append("https://ipinfo.io/{}".format(z.text))

    #print(urls)

    htmls = loop.run_until_complete(fetch_all(urls, loop))

    for i in htmls:
        i = lxml.html.fromstring(i)
        addrss = i.xpath('//div[@id="ipv4-data"]/table[@id="block-table"]/tbody[@class="t-14"]/tr/td[1]/a')
        for a in addrss:
            result.append(a.text)

    f = open("{}.log".format(code),'a')
    for r in result:
        f.write("{}\n".format(r.strip()))
    f.close()

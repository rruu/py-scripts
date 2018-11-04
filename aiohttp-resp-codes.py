import asyncio
import aiohttp
import ssl

timeout = aiohttp.ClientTimeout(total=5)

urls = ['https://google.com','https://youtube.com','https://www.facebook.com/','https://baidu.com', 'https://wikipedia.org','https://reddit.com','https://yahoo.com','https://qq.com','https://taobao.com','https://google.co.in','https://amazon.com','https://tmall.com','https://twitter.com','https://sohu.com','https://instagram.com','https://vk.com','https://live.com','https://jd.com','https://sina.com.cn','https://weibo.com','https://yandex.ru','https://360.cn','https://google.co.jp','https://google.co.uk','https://list.tmall.com','https://google.ru','https://google.com.br','https://netflix.com','https://google.de','https://google.com.hk','https://pornhub.com','https://twitch.tv','https://google.fr','https://linkedin.com','https://yahoo.co.jp','https://t.co','https://csdn.net','https://microsoft.com','https://bing.com','https://office.com','https://ebay.com','https://alipay.com','https://xvideos.com','https://google.it','https://google.ca','https://mail.ru','https://ok.ru','https://google.es','https://pages.tmall.com','https://msn.com','https://google.com.tr','https://google.com.au','https://whatsapp.com','https://spotify.com','https://google.pl','https://google.co.id','https://xhamster.com','https://google.com.ar','https://xnxx.com','https://google.co.th','https://Naver.com','https://sogou.com','https://samsung.com','https://accuweather.com','https://goo.gl','https://sm.cn','https://googleweblight.com' ]

async def fetch(session, url):
    try:
        async with session.get(url, ssl=ssl.SSLContext(), timeout=timeout) as response:
            #return await response.content.read(10)
            print("{} - {}".format(url,response.status))
            #return await response.json()
            return await response.text()
    except Exception:
        print("{} - timeout".format(url))

#async def fetch(session, url):
#    async with session.get(url) as response:
#        #return await response.text()
#        return response.status

async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    htmls = loop.run_until_complete(fetch_all(urls, loop))
    pass
    #print(htmls)
    #for i in htmls:
    #    print(i)

import asyncio
import aiohttp

urls = (('http://httpbin.org/uuid'+' ')*100).split()

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    htmls = loop.run_until_complete(fetch_all(urls, loop))
    #print(htmls[0]['uuid'])
    for i in htmls:
        print(i['uuid'])


from concurrent.futures import ThreadPoolExecutor
import requests

urls = (('https://httpbin.org/uuid'+' ')*100).split()

def uuid(u):
    r = requests.get(u)
    data = r.json()['uuid']
    print(data)

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=50) as pool:
        results = pool.map(uuid, urls)

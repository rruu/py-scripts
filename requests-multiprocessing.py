from multiprocessing import Pool
import requests

urls = (('https://httpbin.org/uuid'+' ')*100).split()

def uuid(u):
    r = requests.get(u)
    data = r.json()['uuid']
    print(data)

if __name__ == '__main__':
    pool = Pool()
    results = pool.map(uuid, urls)
    pool.close()
    pool.join()

import requests
from multiprocessing.dummy import Pool as ThreadPool 

urls = (('https://httpbin.org/uuid'+' ')*100).split()

def uuid(u):
    r = requests.get(u)
    data = r.json()['uuid']
    print(data)

pool = ThreadPool(10) 
results = pool.map(uuid, urls)
pool.close() 
pool.join() 


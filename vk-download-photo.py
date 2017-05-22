#!/usr/bin/python2
# -*- coding: utf-8 -*-

try:
    import vk_api
except ImportError:
    print("Error: module vk_api not found(pip2 install vk_api)")
    exit(1)

try:
    from multiprocessing import Pool
    from multiprocessing.dummy import Pool as ThreadPool
except ImportError:
    print("Error: module multiprocessing not found(pip2 install multiprocessing)")
    exit(1)

import argparse
import requests
import os

USAGE_CONTENT = '%(prog)s [-f args.txt -u user -p qwerty] or [-id 12345 -u user -p qwerty]'
HELP_FILE_CONTENT = 'args.txt: 12345'

vk = None

class PhotoStruct():
    url = ''
    path = ''
    def __init__(self, url, path):
        self.url = url
        self.path = path

def download_and_save_photo(photo_struct):
    content = requests.get(photo_struct.url).content
    with open(photo_struct.path, "wb") as f:
        f.write(content)
    #print(photo_struct.path)

   

def download_albums(vk_id=''):
    path='./Vk'
    try:
        user_id = vk.users.get(user_ids = vk_id)[0]['id']
        print("Start download: {}".format(vk_id))
        vk_id = user_id;
        photoAlbums = vk.photos.getAlbums(owner_id = vk_id, need_system = True)['items']
    except vk_api.ApiError as error_msg:
        print("{} {}".format(vk_id, error_msg))
        return

    for album in photoAlbums:
        i = 0
        path_dir = "{}/{}/{}".format(path, vk_id, album['title'].encode("utf-8"))
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        photos = vk.photos.get(owner_id = vk_id, album_id = album['id'], photo_sizes = True)['items']
        photo_struct_list = []
        for photo in photos:
            biggest = photo['sizes'][0]['width']
            biggestSrc = photo['sizes'][0]['src']
            for size in photo['sizes']:
                if size['width'] > biggest:
                    biggest = size['width']
                    biggestSrc = size['src']
            path_photo =  "{}/{}.jpg".format(path_dir, i)
            photo_struct_list.append(PhotoStruct(biggestSrc, path_photo))
            i += 1
        pool = ThreadPool(10)
        pool.map(download_and_save_photo, photo_struct_list)
        pool.close()
        pool.join()
        print("Complete download: {}".format(vk_id))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vk photo downloader", usage=USAGE_CONTENT)
    parser.add_argument('-f', '--input-file', help=HELP_FILE_CONTENT)
    parser.add_argument('-id', '--vk-id')
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    args = parser.parse_args()


    vk_session = vk_api.VkApi(args.user,  args.password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        exit(1)

    vk = vk_session.get_api()
    vk_api_pool = ThreadPool()
    vk_api_pool = ThreadPool(3)

    if args.input_file:
        with open(args.input_file, "r") as f:
            lines = f.readlines()
            vk_ids = []
            for vk_id in lines:
                vk_id = filter(lambda c: not c.isspace() or c!='\n', vk_id)
                if vk_id:
                    vk_ids.append(vk_id)
                    #download_albums(vk_id)
            results = vk_api_pool.map(download_albums, vk_ids)
            vk_api_pool.close()
            vk_api_pool.join()
    else:
        download_albums(args.vk_id)

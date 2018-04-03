# -*- coding: utf-8 -*-
import socket,sys, re
from multiprocessing.dummy import Pool as ThreadPool
from threading import Lock

if len(sys.argv) < 4 or len(sys.argv) > 4:
    print("Usage: %s iplist.txt 81 out.log" % (str(sys.argv[0])))
    sys.exit(1)

ipaddr = [str(line.strip()) for line in open(sys.argv[1], 'r')]
port = int(sys.argv[2])

def http_banner_grabber(ip, port=80, method="HEAD", timeout=5, http_type="HTTP/1.1"):
    assert method in ['GET', 'HEAD']
    assert http_type in ['HTTP/0.9', "HTTP/1.0", 'HTTP/1.1']
    cr_lf = '\r\n'
    lf_lf = '\n\n'
    crlf_crlf = cr_lf + cr_lf
    res_sep = ''
    rec_chunk = 4096
    s = socket.socket()
    s.settimeout(timeout)
    s.connect((ip, port))
    req_data = "{} / {}{}".format(method, http_type, cr_lf)
    if http_type == "HTTP/1.1":
        req_data += 'Host: {}:{}{}'.format(ip, port, cr_lf)
        req_data += "Connection: close{}".format(cr_lf)
    req_data += cr_lf
    s.sendall(req_data.encode())
    res_data = b''
    while 1:
        try:
            chunk = s.recv(rec_chunk)
            res_data += chunk
        except socket.error:
            break
        if not chunk:
            break
    if res_data:
        res_data = res_data.decode()
    else:
        return '', ''
    if crlf_crlf in res_data:
        res_sep = crlf_crlf
    elif lf_lf in res_data:
        res_sep = lf_lf
    if res_sep not in [crlf_crlf, lf_lf] or res_data.startswith('<'):
        return '', res_data
    content = res_data.split(res_sep)
    banner, body = "".join(content[:1]), "".join(content[1:])
    return banner, body

def parse(ipaddr):
    f = open(sys.argv[3], 'a')
    try:
        result = http_banner_grabber(ipaddr,port)
        if "HTTP" in str(result):
            regex=re.compile(".*(Server:).*")
            parse_result = list(result)
            srv = [m.group(0) for l in parse_result for m in [regex.search(l)] if m]
            print("{},{},{}".format(ipaddr,port,srv[0][8:]), end="\r")
            f.write("{},{},{}\n".format(ipaddr,port,srv[0][8:]))
        else:
            if result[0] == '' and result[1] != '':
                parse_result = list(result)
                print("{},{},{}".format(ipaddr,port,parse_result[1].splitlines().strip()), end="\r")
                f.write("{},{},{}\n".format(ipaddr,port,parse_result[1].splitlines().strip()))
            elif result[0] == '' and result[1] == '':
                pass
    except socket.error:
        pass
    except socket.timeout:
        pass
    except:
        pass
    f.close()

lock = Lock()
pool = ThreadPool(20)

pool.map(parse, ipaddr)
pool.close()
pool.join()

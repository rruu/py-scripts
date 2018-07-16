    # -*- coding: utf-8 -*-
    #!/usr/bin/env python3
    import sys,os

    if len(sys.argv) < 5 or len(sys.argv) > 5:
        print("Usage: %s [Название-лизы] [IPaddr cерверa БРС] [IPaddr БРС] [macaddr БРС вида 080027D15958]" % (str(sys.argv[0])))
        sys.exit(1)

    url1 = '''curl 'https://192.168.1.1:4081/admin/api/jsonrpc/' -H 'Cookie: SESSION_CONTROL_WEBADMIN=d343dddac2bd5bb7d116dc1408618236864c9d90b77b0712b06287e122873444; TOKEN_CONTROL_WEBADMIN=08b695cd5483ec5a88225612839334765239e1fba738cc01d9a6272507d343d3' -H 'Origin: https://192.168.1.1:4081' -H 'Accept-Encoding: gzip, deflate, br' -H 'X-Token: 08b695cd5483ec5a88225612839334765239e1fba738cc01d9a6272507d343d3' -H 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json-rpc' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://192.168.1.1:4081/admin/' --data-binary $'{"jsonrpc":"2.0","id":1,"method":"Dhcp.createLeases","params":{"leases":[{"name":'''

    name = str(sys.argv[1])

    url2 = ''',"leaseId":"","scopeId":"","status":"StoreStatusNew","type":"DhcpTypeReservation","leased":false,"isRas":false,"options":[{"value":'''

    brsserver = str(sys.argv[2])

    url3 = ''',"type":"DhcpString","ipListList":[],"optionId":66,"name":"TFTP server name","isLease":true,"isDuplicate":""}],"ipAddress":'''

    brsclientip = str(sys.argv[3])

    url4 = ''',"macDefined":true,"macAddress":'''

    macaddr = str(sys.argv[4])

    url5 = ''',"hostName":"","userName":"","cardManufacturer":"","expirationDate":{"year":0,"month":0,"day":0},"expirationTime":{"hour":0,"min":0},"requestDate":{"year":0,"month":0,"day":0},"requestTime":{"hour":0,"min":0}}]}}' --compressed --insecure '''


    #os.system("{}{}{}{}{}{}{}{}{}".format(url1,name,url2,brsserver,url3,brsclientip,url4,macaddr,url5))
    print("{}\"{}\"{}\"{}\"{}\"{}\"{}\"{}\"{}".format(url1,name,url2,brsserver,url3,brsclientip,url4,macaddr,url5))

    '''
    # Пример запроса:
    curl 'https://192.168.1.1:4081/admin/api/jsonrpc/' -H 'Cookie: SESSION_CONTROL_WEBADMIN=1a060a277a9e603360203e10a349d6f95741b169e91229c9de30075289bdf064; TOKEN_CONTROL_WEBADMIN=6f51e138912a8911977907be37d912d48ab6bc1125c506398f616bbb47fd5635' -H 'Origin: https://192.168.1.1:4081' -H 'Accept-Encoding: gzip, deflate, br' -H 'X-Token: 6f51e138912a8911977907be37d912d48ab6bc1125c506398f616bbb47fd5635' -H 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json-rpc' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Referer: https://192.168.1.1:4081/admin/' --data-binary $'{"jsonrpc":"2.0","id":1,"method":"Dhcp.createLeases","params":{"leases":[{"name":
    name = "Иванов-МРЦОД будущий"

    ,"leaseId":"","scopeId":"","status":"StoreStatusNew","type":"DhcpTypeReservation","leased":false,"isRas":false,"options":[{"value":
    brsserver = "192.168.63.115"

    ,"type":"DhcpString","ipListList":[],"optionId":66,"name":"TFTP server name","isLease":true,"isDuplicate":""}],"ipAddress":
    brsclientip = "192.168.201.121"

    ,"macDefined":true,"macAddress":
    macaddr = "080027D15951"

    ,"hostName":"","userName":"","cardManufacturer":"","expirationDate":{"year":0,"month":0,"day":0},"expirationTime":{"hour":0,"min":0},"requestDate":{"year":0,"month":0,"day":0},"requestTime":{"hour":0,"min":0}}]}}' --compressed --insecure
    '''

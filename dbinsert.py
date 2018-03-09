#!/usr/bin/env python3
# require
# pip3 install psycopg2-binary

import psycopg2
import sys

#check args
if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Usage: %s data.txt" % (str(sys.argv[0])))
    sys.exit(1)

#db config
host = "xxx"
dbname = "xxx"
user = "xxx"
password = "xxx"

conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,user,host,password))

f = [line.strip() for line in open(sys.argv[1], 'r')]
f = [x for x in f if x]

data = []

try:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE headers(
        id bigserial PRIMARY KEY,
        ipaddr inet,
        port smallint,
        header text
    )
    """)
except:
    print("table created")
    conn.commit()

try:
    cur = conn.cursor()
    for line in f:
        ipaddr = line.split(",")[0]
        port = line.split(",")[1]
        header = str(line.split(",")[2]).strip().replace("'", "")
        insert_query = "INSERT INTO headers (ipaddr,port,header) values ('{}','{}','{}');\r".format(ipaddr,port,header).strip()
        data.append(insert_query.strip())
        print("INSERT COMPLETE")
except:
    print("INSERT ERR")
#print(''.join(map(str, data)))
cur.execute(''.join(map(str, data)))
conn.commit()

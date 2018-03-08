import psycopg2
import sys

#db config
host = "xxx"
dbname = "xxx"
user = "xxx"
password = "xxx"

conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,user,host,password))

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
    with open(sys.argv[1]) as f:
        for line in f:
            ipaddr = line.split(",")[0]
            port = line.split(",")[1]
            header = str(line.split(",")[2]).strip().replace("'", "")
            #print('{} {} {}'.format(ipaddr,port,header).rstrip())
            insert_query = "INSERT INTO headers (ipaddr,port,header) values ('{}','{}','{}');\r".format(ipaddr,port,header).strip()
            data.append(insert_query.strip())
except:
    print("INSERT PROBLEM")
#print(''.join(map(str, data)))
cur.execute(''.join(map(str, data)))
conn.commit()


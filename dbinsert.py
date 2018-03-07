import psycopg2

#db config
host = "xxx"
dbname = "xxx"
user = "xxx"
password = "xxx"


conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(dbname,user,host,password))

# create table
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
    #cur.rollback()

try:
    cur = conn.cursor()
    with open("ok.log") as f:
        for line in f:
            ipaddr = line.split(",")[0]
            port = line.split(",")[1]
            header = str(line.split(",")[2])
            print('{} {} {}'.format(ipaddr,port,header).rstrip())
            insert_query = "INSERT INTO headers (ipaddr,port,header) values ('{}','{}','{}');".format(ipaddr,port,header)
            cur.execute(insert_query)
    
    conn.commit()
except:
    print("INSERT PROBLEM")

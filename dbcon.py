
try:
    import mysql as my
    from mysql import connector as mycon
except ImportError as e:
    print("mysql-connector-python module doesn't exist")
    print(e)
    exit()

def conDB():
    mydb=None
    try:
        hostname=username=passw=dbname=""
        f=open("dbinfo.txt","r")
        for r in f:
            sl = r.split(":")
            key=sl[0].strip()
            val=sl[1].strip()
            if key == "host":
                hostname=str(val)
            if key == "user":
                username=val
            if key == "password":
                if val is None:
                    passw = ""
                else:
                    passw=val
            if key == "database":
                dbname=val

        mydb = mycon.connect(
        host=hostname,
        user=username,
        password=passw,
        database=dbname
        )
        return mydb
    except Exception as e:
        print("Cannot establish a connection with Database !!. Contact Admin")
        print(e)
        exit()

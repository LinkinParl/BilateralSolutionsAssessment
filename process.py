import dbcon
import os
import time
import shutil
import threading as th

global lastcnt
global i
global curdir
global dbcurr
global db
i=1
lastcnt=0
db=dbcon.conDB()
dbcurr = db.cursor(buffered=True)
try:
    dbcurr.execute("select count(*) from filestatus")
    filecnt = dbcurr.fetchone()
    lastcnt=filecnt[0] # storing last entry id, to continue with filenaming convention
except Exception as e:
    print("Could not execute query !!")
    print(e)
    exit()

#create folders if doesn't exist
curdir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(curdir+"/processing"):
    os.mkdir(curdir+"/processing")
if not os.path.exists(curdir+"/processed"):
    os.mkdir(curdir+"/processed")
if not os.path.exists(curdir+"/queue"):
    os.mkdir(curdir+"/queue")


#function to create a file
def createFile(i):
    print("Creating file {}...".format(lastcnt+i))
    f = open("{0}/processing/file{1}.txt".format(curdir,lastcnt+i), "w")
    f.write("Created this file for demo assessment !!")
    f.close()
    print("File created !!\n")
    sql = "INSERT INTO filestatus (filename) VALUES (%s)"
    val = ["file{0}.txt".format(lastcnt+i)]
    try:
        dbcurr.execute(sql, val)
        db.commit()
    except Exception as e:
        print("Could not execute query !!\n")
        print(e)
        exit()
    th.Timer(1, createFile,[i+1]).start()

#function to move files to queue folder
def addFiletoQueue():
    allprocessing = os.listdir("{0}/processing".format(curdir))
    queuedfiles = os.listdir("{0}/queue".format(curdir))
    if len(queuedfiles) <= 0:
        print("Moving files [{0} - {1}] to queue folder...".format(allprocessing[0],allprocessing[-1]))
        for f in allprocessing:
            shutil.move("{0}/processing/{1}".format(curdir,f), "{0}/queue/{1}".format(curdir,f))

        print("Files moved to queue folder !!\n")
    else:
        print("Queue folder not empty !! Cannot move files from processing to queue")
    processFile()
    th.Timer(5, addFiletoQueue).start()

#function to update and move files to processed folder
def processFile():
    allqueue = os.listdir("{0}/queue".format(curdir))
    print("Updating file statuses [{0} - {1}] !!".format(allqueue[0],allqueue[-1]))
    sql = "UPDATE filestatus SET status = '1' WHERE filename = %s"
    values=[]
    for f in allqueue:
        values.append([f])
    try:
        dbcurr.executemany(sql, values)
        db.commit()
        print("Updated successfully\n")
        print("Moving files to processed folder after updation")
        for f in allqueue:
            shutil.move("{0}/queue/{1}".format(curdir,f), "{0}/processed/{1}".format(curdir,f))
    
    except Exception as e:
        print("Could not update status for processed files !!\n")
        print(e)
        exit()

    print("Done !!\n")
    time.sleep(2) # just a delay in clear screen to read content on terminal
    os.system("cls")

# created 2 async threads
th.Timer(1, createFile,[i]).start() # create 1 file every 1 sec
th.Timer(5, addFiletoQueue).start() # move files to queue every 5 secs


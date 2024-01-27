import time
import sys
import sqlite3
from datetime import date
from datetime import datetime 



def secToHours(seconds):
	seconds = seconds % (24 * 3600)
	hr = seconds // 3600
	seconds %= 3600
	min = seconds // 60
	seconds %= 60

	duration = "%d:%02d:%02d" % (hr, min, seconds)
	return duration


def differenceOfTime(start,end):
	start = datetime.strptime(start, "%H:%M:%S") 
	end = datetime.strptime(end, "%H:%M:%S") 

	difference = end - start 

	seconds = difference.total_seconds()
	return seconds 


# Getting Current Time
time = time.localtime()
time = str(time.tm_hour) + ":" + str(time.tm_min) + ":" + str(time.tm_sec)

# Getting Date
today = date.today()
today = today.strftime("%d/%m/%Y")

# Connecting to DB
connection = sqlite3.connect("/home/ubuntu/screenTime/screenTime.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS EntryExitDetails(date TEXT, entry_time TEXT, exit_time TEXT, diff INTEGER)")
cursor = connection.cursor()

# Adding Entry Time
if(sys.argv[1] == 'start'):
	cursor.execute("INSERT INTO EntryExitDetails VALUES(?,?,?,?)",(today,time,"0",0))


# Adding Exit Time 
if(sys.argv[1] == 'end'):
	rowID = cursor.execute("SELECT ROWID from EntryExitDetails WHERE date = ? ORDER BY ROWID DESC LIMIT 1",(today,)).fetchone()[0]
	startTime = cursor.execute("SELECT entry_time from EntryExitDetails WHERE ROWID = ?",(rowID,)).fetchone()[0]
	seconds = differenceOfTime(start=startTime,end=time)
	insertTime = cursor.execute("UPDATE EntryExitDetails SET exit_time = ? , diff = ? WHERE ROWID = ?",(time,seconds,rowID,))


rows = cursor.execute("SELECT * from EntryExitDetails").fetchall()
print(rows[-1])

connection.commit()

print("Time : "+time)



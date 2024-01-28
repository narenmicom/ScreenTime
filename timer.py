import time
import sys
import sqlite3
from datetime import date
from datetime import datetime 
import platform

currentPlatform = platform.system()

if currentPlatform is "Windows":
	dbLocation = "screenTime.db"
else:
	dbLocation = "/home/ubuntu/screenTime/screenTime.db"


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



dbLocation = "asd"

# Connecting to DB
connection = sqlite3.connect(dbLocation)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS EntryExitDetails(date TEXT, entry_time TEXT, exit_time TEXT, diff INTEGER)")
cursor = connection.cursor()

# Adding Entry Time
if(sys.argv[1] == 'start'):
	toCheck = cursor.execute("SELECT * FROM EntryExitDetails ORDER BY ROWID DESC LIMIT 1").fetchall()[0][3]
	cursor.execute("INSERT INTO EntryExitDetails VALUES(?,?,?,?)",(today,time,"0",0)) if toCheck != 0 else exit
	

# Adding Exit Time 
if(sys.argv[1] == 'end'):
	rowID = cursor.execute("SELECT ROWID from EntryExitDetails WHERE date = ? ORDER BY ROWID DESC LIMIT 1",(today,)).fetchone()[0]
	startTime = cursor.execute("SELECT entry_time from EntryExitDetails WHERE ROWID = ?",(rowID,)).fetchone()[0]
	seconds = differenceOfTime(start=startTime,end=time)
	insertTime = cursor.execute("UPDATE EntryExitDetails SET exit_time = ? , diff = ? WHERE ROWID = ?",(time,seconds,rowID,))

if(sys.argv[1] == 'howMuch'):
	totalDuration = cursor.execute("SELECT SUM(diff) from EntryExitDetails WHERE date = ?",(today,)).fetchall()
	print(totalDuration[0][0])

rows = cursor.execute("SELECT * from EntryExitDetails").fetchall()
print(rows[-1])


connection.commit()

print("Time : "+time)



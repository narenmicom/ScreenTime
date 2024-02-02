import time
import sys
import sqlite3
from datetime import date
from datetime import datetime 
import platform

currentPlatform = platform.system()

if currentPlatform == "Windows":
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

# Connecting to DB
connection = sqlite3.connect(dbLocation)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sessions(date TEXT, entry_time TEXT, exit_time TEXT, diff INTEGER)")
cursor = connection.cursor()

# Adding Entry Time
if(sys.argv[1] == 'start'):
	try:
		toCheck = cursor.execute("SELECT exit_time FROM sessions ORDER BY ROWID DESC LIMIT 1").fetchall()
		toCheck = len(toCheck[0][0])
		exit if toCheck == 1 else cursor.execute("INSERT INTO sessions VALUES(?,?,?,?)",(today,time,"0",0))
	except:
		cursor.execute("INSERT INTO sessions VALUES(?,?,?,?)",(today,time,"0",0))

# Adding Exit Time
if(sys.argv[1] == 'end'):
	rowID = cursor.execute("SELECT ROWID from sessions WHERE date = ? ORDER BY ROWID DESC LIMIT 1",(today,)).fetchone()[0]
	startTime = cursor.execute("SELECT entry_time from sessions WHERE ROWID = ?",(rowID,)).fetchone()[0]
	seconds = differenceOfTime(start=startTime,end=time)
	insertTime = cursor.execute("UPDATE sessions SET exit_time = ? , diff = ? WHERE ROWID = ?",(time,seconds,rowID,))

if(sys.argv[1] == 'used'):
	if(sys.argv[2] == 'today'):
		totalDuration = cursor.execute("SELECT SUM(diff) from sessions WHERE date = ?",(today,)).fetchall()
		totalDuration = totalDuration[0][0]
		print(secToHours(totalDuration))
	if(sys.argv[2] == "on"):
		date = sys.argv[3]
		totalDuration = cursor.execute("SELECT SUM(diff) from sessions WHERE date = ?",(date,)).fetchall()
		totalDuration = totalDuration[0][0]
		print(secToHours(totalDuration))


print(cursor.execute("SELECT * FROM sessions ORDER BY ROWID DESC LIMIT 1").fetchall())


connection.commit()

print("Time : "+time)



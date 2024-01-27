import time
import sys
import sqlite3
from datetime import date


def secToHours(seconds):
	seconds = seconds % (24 * 3600)
	hr = seconds // 3600
	seconds %= 3600
	min = seconds // 60
	seconds %= 60

	duration = "%d:%02d:%02d" % (hr, min, seconds)
	return duration


print(secToHours(45.0))


# Getting Current Time
time = time.localtime()
time = str(time.tm_hour) + ":" + str(time.tm_min) + ":" + str(time.tm_sec)

# Getting Date
today = date.today()
today = today.strftime("%d/%m/%Y")

# Connecting to DB
connection = sqlite3.connect("/home/ubuntu/screenTime/screenTime.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS EntryExitDetails(date TEXT, entry_time TEXT, exit_time TEXT)")
cursor = connection.cursor()

# Adding Entry Time
if(sys.argv[1] == 'start'):
	cursor.execute("INSERT INTO EntryExitDetails VALUES(?,?,?)",(today,time,"0"))


# Adding Exit Time 
if(sys.argv[1] == 'end'):
	op = cursor.execute("SELECT ROWID from EntryExitDetails WHERE date = ? ORDER BY ROWID DESC LIMIT 1",(today,)).fetchone()
	rowID = op[0]
	insertTime = cursor.execute("UPDATE EntryExitDetails SET exit_time = ? WHERE ROWID = ?",(time,rowID,))


rows = cursor.execute("SELECT * from EntryExitDetails").fetchall()
print(rows[-1])

connection.commit()

print("Time : "+time)



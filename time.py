import time
import sys
import sqlite3
from datetime import date


# Getting Current Time
time = time.localtime()
time = str(time.tm_hour) + ":" + str(time.tm_min) + ":" + str(time.tm_sec)

# Getting Date
today = date.today()
today = today.strftime("%d/%m/%Y")

# Connecting to DB
connection = sqlite3.connect("screenTime.db")
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
print(rows)

connection.commit()

print("Time : "+time)

import sqlite3
from datetime import date

def insertTime():
	connection = sqlite3.connect("screenTime.db")

	today = date.today()
	today = today.strftime("%d/%m/%Y")
	print(type(today))
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS EntryExitDetails(date TEXT, entry_time TEXT, exit_time TEXT)")
	cursor.execute("INSERT INTO EntryExitDetails VALUES(?,?,?)",(today,"19:31","21:02"))
	rows = cursor.execute("SELECT * from EntryExitDetails").fetchall()
	print(rows)
	connection.commit()

insertTime()

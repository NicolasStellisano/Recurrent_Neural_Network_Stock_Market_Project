import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE predictions (symbol TEXT, date TEXT, json TEXT)')
print ("Table created successfully")
conn.close()
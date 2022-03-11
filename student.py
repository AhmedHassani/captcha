import sqlite3

conn = sqlite3.connect('db.db')
cur = conn.cursor()
data = cur.execute("SELECT * from admin")
for d in data.fetchall():
    print(d)
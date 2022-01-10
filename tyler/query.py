import sqlite3

conn = sqlite3.connect('../options.db')

c = conn.cursor()

statement = ''
c.execute(statement)

conn.commit()

conn.close()
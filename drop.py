import sqlite3

conn = sqlite3.connect('face.db')

conn.execute('''DROP TABLE TEACHERS_ATTENDANCE''')
conn.close()
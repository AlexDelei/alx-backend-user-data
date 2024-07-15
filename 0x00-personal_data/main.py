#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db
RedactingFormatter = __import__('filtered_logger').RedactingFormatter


db = get_db()
cursor = db.cursor()

cursor.execute("SHOW COLUMNS FROM users;")
columns = [column[0] for column in cursor.fetchall()]

cursor.execute("SELECT * FROM users;")
records = cursor.fetchall()

print("\t".join(columns))

for record in records:
    print("\t".join(str(field) for field in record))


cursor.close()
db.close()

#!/usr/bin/env python3
"""
Main file
"""
import logging

get_db = __import__('filtered_logger').get_db
RedactingFormatter = __import__('filtered_logger').RedactingFormatter


db = get_db()
cursor = db.cursor()

cursor.execute("SHOW COLUMNS FROM users;")
columns = [column[0] for column in cursor.fetchall()]

cursor.execute("SELECT * FROM users;")
records = cursor.fetchall()

for record in records:
    formatted_record = "; ".join(f"{col}='{val}'" for col, val in zip(columns, record)) + ";"
    log_record = logging.LogRecord("my_logger", logging.INFO, None, None, formatted_record, None, None)
    formatter = RedactingFormatter(fields=("name", "email", "phone", "ssn", "password"))
    print(formatter.format(log_record))


cursor.close()
db.close()

#!/usr/bin/env python3
"""Regex-ing"""
from typing import List
from mysql.connector.connection import MySQLConnection
from mysql.connector import connection
from os import getenv
import re
import logging

"""
Write a function called filter_datum that returns the log message obfuscated:

Arguments:
fields: a list of strings representing all fields to obfuscate
redaction: a string representing by what the field will be obfuscated
message: a string representing the log line

separator: a string representing by which character is separating
all fields in the log line (message)

The function should use a regex to replace occurrences of certain field values.
filter_datum should be less than 5 lines long and use re.sub to
perform the substitution with a single regex.
"""

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Using regex to replace certain occure"""
    pattern = r'(' + '|'.join([f'{f}=[^{separator}]*' for f in fields]) + r')'
    return re.sub(
        pattern,
        lambda m: m.group().split('=')[0] + '=' + redaction,
        message
        )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Log formatter - Initiator"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Log formatter - when formatting"""
        msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


"""
Implement a get_logger function that
takes no arguments and returns a logging.Logger object.

The logger should be named "user_data" and
only log up to logging.INFO level.
It should not propagate messages to other loggers.
It should have a StreamHandler with RedactingFormatter as formatter.

Create a tuple PII_FIELDS constant at the root of the module
containing the fields from user_data.csvthat are considered
PII. PII_FIELDS can contain only 5 fields -
choose the right list of fields that can are
considered as “important” PIIs or information that you must hide in your logs.
Use it to parameterize the formatter.
"""
"""
PseudoCode:
## Define the PII_FIELDS tuple
STEP 1: Choosing the fields from user_data.csv that are considered PII

EXPLANATION:
The PII_FIELDS are defined at the root of the module
to contain the fields considered PII


## Implemeting the get_logger function
STEP 1: Create a Logger named 'user_data'
STEP 2: Set the logger level to logging.INFO
STEP 3: Ensure the logger does not propagate messages to other loggers.
STEP 4: Add a StreamHandler with RedactingFormatter as the formatter.
STEP 5: Parameterize the formatter with the PII fields.


EXPLANATION:
Creates a logger named "user_data".
Sets the logger level to logging.INFO.
Disables message propagation to other loggers.
Adds a StreamHandler with RedactingFormatter configured with PII_FIELDS.
Returns the configured logger.

"""


def get_logger() -> logging.Logger:
    """
    Creating a logger with certain requirements
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    # logger.propagate = False ; prevents messages from
    # being propagated to other loggers

    stream_handler = logging.StreamHandler()

    # setting the formatter
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # adding handler to the Logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    MySQL connection object - connection.MYSQLConnection()

    return:
        the connection object
    """
    user = getenv("PERSONAL_DATA_DB_USERNAME")
    pswd = getenv("PERSONAL_DATA_DB_PASSWORD")
    host = getenv("PERSONAL_DATA_DB_HOST")
    db = getenv("PERSONAL_DATA_DB_NAME")

    conn = connection.MySQLConnection(
        user=user,
        password=pswd,
        host=host,
        database=db
    )
    return conn


"""
The function will obtain a database connection using get_db and
retrieve all rows in the users table and display each row under
a filtered format
"""


def main():
    """
    Read and filter data
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SHOW COLUMNS FROM users;")
    columns = [column[0] for column in cursor.fetchall()]

    cursor.execute("SELECT * FROM users;")
    records = cursor.fetchall()

    for record in records:
        formatted_record = "; ".join(
            f"{col}='{val}'" for col, val in zip(columns, record)) + ";"
        log_record = logging.LogRecord(
            "user_data",
            logging.INFO,
            None,
            None,
            formatted_record,
            None,
            None
            )
        formatter = RedactingFormatter(
            fields=("name", "email", "phone", "ssn", "password")
            )
        print(formatter.format(log_record))

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()

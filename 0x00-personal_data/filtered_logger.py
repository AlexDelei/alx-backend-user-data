#!/usr/bin/env python3
"""Regex-ing"""
from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Using regex to replace certain occure"""
    pattern = r'(' + '|'.join([f'{f}=[^{separator}]*' for f in fields]) + r')'
    return re.sub(pattern, lambda m: m.group().split('=')[0] + '=' + redaction, message)


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

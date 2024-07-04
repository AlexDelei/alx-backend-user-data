#!/usr/bin/env python3
"""Regex-ing"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Using regex to replace certain occure"""
    pattern = r'(' + '|'.join([f'{f}=[^{separator}]*' for f in fields]) + r')'
    return re.sub(pattern, lambda m: m.group().split('=')[0] + '=' + redaction, message)

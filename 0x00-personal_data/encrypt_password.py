#!/usr/bin/env python3
"""
Encrypting passwords
"""
from typing import ByteString
import bcrypt


def hash_password(password: str) -> ByteString:
    """
    hashes and salts a password and turns it
    into a byte string
    """
    paswd_b_string = password.encode()
    hashed = bcrypt.hashpw(paswd_b_string, bcrypt.gensalt(14))

    return hashed

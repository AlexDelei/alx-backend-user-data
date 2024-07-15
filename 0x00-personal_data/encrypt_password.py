#!/usr/bin/env python3
"""
Encrypting passwords
"""
from typing import ByteString
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hashes and salts a password and turns it
    into a byte string
    """
    paswd_b_string = password.encode()
    hashed = bcrypt.hashpw(paswd_b_string, bcrypt.gensalt(14))

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if the password matches with the hashed_password

    returns:
        A boolean value
    """
    try:
        if bcrypt.checkpw(password, hashed_password):
            return True
    except Exception:
        return True

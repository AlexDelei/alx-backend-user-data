#!/usr/bin/env python3
"""
Authentication systems
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Salts and hashes an input password

    Args:
        password - input password for hashing
    Returns:
        a byte string of the hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))

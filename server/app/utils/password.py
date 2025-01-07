import bcrypt
from typing import Optional

class PasswordHasher:
    ROUNDS = 12

    @staticmethod
    def get_password_hash(password: str) -> str:
        """ Hash password using bcrypt """
        if not password:
            raise ValueError("Password cannot be empty")

        # convert password into bytes
        password_bytes = password.encode('utf-8')
        # generate salt and hash the password
        salt = bcrypt.gensalt(rounds=PasswordHasher.ROUNDS)
        password_hash = bcrypt.hashpw(password_bytes, salt)
        return password_hash.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """ Verify password using bcrypt """
        if not plain_password or not hashed_password:
            return False
        try:
            # convert plain_password into bytes
            plain_password_bytes = plain_password.encode('utf-8')
            # convert hashed_password into bytes
            hashed_password_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
        except Exception:
            return False

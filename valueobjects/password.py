from dataclasses import dataclass
import bcrypt
import base64

@dataclass
class Password:

    def __init__(self, hash: str):
        self.hashed_pw: str = hash

    def compare(self, password: str) -> bool:
        hashed_password_bytes = base64.b64decode(self.hashed_pw.encode('utf-8'))
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password_bytes)

    @staticmethod
    def from_password(password: str):

        salt = bcrypt.gensalt(12)
        hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
        hashed_password_string = base64.b64encode(hashed_password_bytes).decode('utf-8')
        return Password(hashed_password_string)

    @staticmethod
    def from_hash(hash: str):
        return Password(hash)

# password hashing package
import bcrypt
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hass_password(password: str):
    return pwd_context.hash(password)
    # pwd_bytes = password.encode('utf-8')
    # salt = bcrypt.gensalt()
    # hashed_password = bcrypt.hashpw(pwd_bytes, salt=salt)
    # return hashed_password
    # # return pwd_context.hash(password)

def compare_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    
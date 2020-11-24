from passlib.context import CryptContext


# This will be used for hash the passwords
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return pwd_context.hash(password)

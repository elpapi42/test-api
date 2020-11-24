from jose import jwt
from passlib.context import CryptContext
from fastapi import Request, HTTPException, Depends

from api import settings


# This will be used for hash and verify the passwords
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

class Autheticate():
    """Authenticate incoming request."""
    def __init__(self, request: Request):
        header = request.headers.get('Authorization')
        if (not header):
            raise HTTPException(401, 'unathorized')

        token_type, token = header.split()

        if token_type.lower() != 'bearer':
            raise HTTPException(401, 'this api only support bearer tokens')

        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError as err:
            raise HTTPException(401, 'token expired')
        except jwt.JWTClaimsError:
            raise HTTPException(401, 'token has invalid claims')
        except jwt.JWTError:
            raise HTTPException(401, 'unable to validate token')

        self.id = payload.get('sub')
        self.admin = payload.get('adm')

class IsAdmin():
    """Ensures the user is admin."""
    def __init__(self, auth: Autheticate = Depends()):
        
        if not auth.admin:
            raise HTTPException(401, 'unathorized')

        self.id = auth.id
        self.admin = auth.admin

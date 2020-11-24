from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Response
from jose import jwt

from api.database import db
from api.schemas.login import LoginSchema, TokenSchema
from api.auth import verify_password
from api import settings


router = APIRouter()

@router.post('/', response_model=TokenSchema)
async def create_user(data: LoginSchema):
    # Fetch user from db
    user = db.users.find_one({'email': data.email})

    if not user:
        raise HTTPException(status_code=404, detail='user not registered')

    if not verify_password(data.password, user['password']):
        raise HTTPException(status_code=401, detail='invalid password')

    token = jwt.encode(
        {
            'exp': datetime.now(timezone.utc) + timedelta(hours=6),
            # Embed on the token if the user is an admin
            'adm': user.get('superadmin') or False
        },
        key=settings.SECRET_KEY,
        algorithm='HS256'
    )

    return {'token': token, 'token_type': 'bearer'}

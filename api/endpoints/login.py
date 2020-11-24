from fastapi import APIRouter, HTTPException, Response

from api.database import db
from api.schemas.login import LoginSchema, TokenSchema
from api.auth import verify_password


router = APIRouter()

@router.post('/', response_model=TokenSchema)
async def create_user(data: LoginSchema):
    # Fetch user from db
    user = db.users.find_one({'email': data.email})

    if not user:
        raise HTTPException(status_code=404, detail='user not registered')

    if not verify_password(data.password, user['password']):
        raise HTTPException(status_code=401, detail='invalid password')

    return {'token': 'test'}

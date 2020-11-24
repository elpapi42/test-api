from typing import List

from fastapi import APIRouter, HTTPException, Response, Depends, status
from pymongo import errors

from api.database import db
from api.schemas.users import CreateUserSchema, UserSchema


router = APIRouter()

@router.post('/', response_model=UserSchema)
async def create_user(data: CreateUserSchema):
    try:
        user = db.users.insert_one(data.dict())
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='email already registered'
        )

    return data

@router.get('/', response_model=List[UserSchema])
async def list_users():
    users = db.users.find()
    users = [user for user in users]
    return users

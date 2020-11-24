from typing import List

from fastapi import APIRouter, HTTPException, Response, Depends, status
from pymongo import errors
from bson.objectid import ObjectId

from api.database import db
from api.schemas.users import CreateUserSchema, UserSchema, UpdateUserSchema
from api.auth import hash_password, Autheticate

router = APIRouter()


@router.post('/', response_model=UserSchema)
async def create_user(data: CreateUserSchema):
    # Hash the password
    data.password = hash_password(data.password)

    try:
        user = db.users.insert_one(data.dict())
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='email already registered'
        )

    return {'id': str(user.inserted_id), **data.dict()}

@router.get('/', response_model=List[UserSchema])
async def list_users():
    users = db.users.find()
    users = [{'id': str(user.get('_id')), **user} for user in users]
    return users

@router.get('/{id}/', response_model=UserSchema)
async def retrieve_user(id: str, auth:  = Depends(Autheticate)):
    try:
        # Fetch user from db
        user = db.users.find_one({'_id': ObjectId(id)})
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='invalid id')

    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    # Appends id with pydantic compatible name
    user['id'] = str(user['_id'])

    return user

@router.patch('/{id}/')
async def update_user(id: str, data: UpdateUserSchema):
    if data.password:
        # Hash the password
        data.password = hash_password(data.password)

    try:
        # Update user data in db
        result = db.users.update_one(
            {'_id': ObjectId(id)},
            {'$set': data.dict(exclude_unset=True)}
        )
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='invalid id')

    if result.matched_count <= 0:
        raise HTTPException(status_code=404, detail='user not found')

    return Response(status_code=204)

@router.delete('/{id}/')
async def delete_user(id: str):
    try:
        # delete user data in db
        result = db.users.delete_one({'_id': ObjectId(id)})
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='invalid id')

    if result.deleted_count <= 0:
        raise HTTPException(status_code=404, detail='user not found')

    return Response(status_code=204)

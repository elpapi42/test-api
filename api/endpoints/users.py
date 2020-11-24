from typing import List

from fastapi import APIRouter, HTTPException, Response, Depends
from pymongo import errors
from bson.objectid import ObjectId

from api.database import db
from api.schemas.users import CreateUserSchema, UserSchema, UpdateUserSchema
from api.auth import hash_password, Autheticate, IsAdmin

router = APIRouter()


@router.post('/', response_model=UserSchema)
async def create_user(data: CreateUserSchema):
    # Hash the password
    data.password = hash_password(data.password)

    if (data.company_id):
        data.company_id = ObjectId(data.company_id)

    try:
        user = db.users.insert_one(data.dict())
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail='email already registered'
        )

    return {'id': str(user.inserted_id), **data.dict()}

@router.get('/', response_model=List[UserSchema])
async def list_users(auth: IsAdmin = Depends()):
    users = db.users.find()
    # Convert to list of users and injects id with correct naming
    users = [{'id': str(user.get('_id')), **user} for user in users]
    return users

@router.get('/{id}/', response_model=UserSchema)
async def retrieve_user(id: str, auth: Autheticate = Depends()):
    # If the requester is not admin, and not owner of this account
    if not auth.admin and auth.id != id:
        raise HTTPException(status_code=401, detail='unauthorized')

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
async def update_user(id: str, data: UpdateUserSchema, auth: Autheticate = Depends()):
    # If the requester is not admin, and not owner of this account
    if not auth.admin and auth.id != id:
        raise HTTPException(status_code=401, detail='unauthorized')

    if data.password:
        # Hash the password
        data.password = hash_password(data.password)
    
    # normal users cant update themselves to admins
    if data.admin and not auth.admin:
        # Remove admin flag
        data.admin = False

    if (data.company_id):
        data.company_id = ObjectId(data.company_id)

    try:
        # Update user data in db
        result = db.users.update_one(
            {'_id': ObjectId(id)},
            {'$set': data.dict(exclude_unset=True)}
        )
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='invalid id')
    except errors.WriteError:
        raise HTTPException(status_code=400, detail='nothing to update')

    if result.matched_count <= 0:
        raise HTTPException(status_code=404, detail='user not found')

    return Response(status_code=204)

@router.delete('/{id}/')
async def delete_user(id: str, auth: IsAdmin = Depends()):
    try:
        # delete user data in db
        result = db.users.delete_one({'_id': ObjectId(id)})
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='invalid id')

    if result.deleted_count <= 0:
        raise HTTPException(status_code=404, detail='user not found')

    return Response(status_code=204)

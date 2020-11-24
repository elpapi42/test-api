from typing import List

from fastapi import APIRouter, HTTPException, Response, Depends

from api.database import db


router = APIRouter()

@router.get('/')
async def get_users():
    users = db.users.find()
    return users
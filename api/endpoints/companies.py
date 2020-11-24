from typing import List

from fastapi import APIRouter, HTTPException, Response, Depends
from pymongo import errors
from bson.objectid import ObjectId

from api.database import db
from api.schemas.companies import CompanySchema, WriteCompanySchema
from api.auth import Autheticate, IsAdmin


router = APIRouter()

@router.post('/', response_model=CompanySchema)
async def create_user(data: WriteCompanySchema, auth: IsAdmin = Depends()):
    try:
        company = db.companies.insert_one(data.dict())
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='company ith this name already registered'
        )

    return {'id': str(company.inserted_id), **data.dict()}

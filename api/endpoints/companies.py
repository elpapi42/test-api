from typing import List

from fastapi import APIRouter, HTTPException, Response, Depends
from pymongo import errors
from bson.objectid import ObjectId

from api.database import db
from api.schemas.companies import CompanySchema, WriteCompanySchema
from api.auth import Autheticate, IsAdmin


router = APIRouter()

@router.post('/', response_model=CompanySchema)
async def create_company(data: WriteCompanySchema, auth: IsAdmin = Depends()):
    try:
        company = db.companies.insert_one(data.dict())
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail='company ith this name already registered'
        )

    return {'id': str(company.inserted_id), **data.dict()}

@router.get('/', response_model=List[CompanySchema])
async def list_companies(auth: Autheticate = Depends()):
    companies = db.companies.find()
    companies = [{'id': str(company.get('_id')), **company} for company in companies]
    return companies

@router.get('/{id}/', response_model=CompanySchema)
async def retrieve_company(id: str, auth: Autheticate = Depends()):
    try:
        # Fetch company from db
        company = db.companies.find_one({'_id': ObjectId(id)})
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='invalid id')

    if not company:
        raise HTTPException(status_code=404, detail='company not found')

    # Appends id with pydantic compatible name
    company['id'] = str(company['_id'])

    return company

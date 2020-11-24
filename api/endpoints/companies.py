from typing import List

from fastapi import APIRouter, HTTPException, Response, Depends
from pymongo import errors
from bson.objectid import ObjectId

from api.database import db
from api.schemas.companies import CompanySchema, CreateCompanySchema, UpdateCompanySchema
from api.auth import Autheticate, IsAdmin


router = APIRouter()

@router.post('/', response_model=CompanySchema)
async def create_company(data: CreateCompanySchema, auth: IsAdmin = Depends()):
    try:
        company = db.companies.insert_one(data.dict())
    except errors.DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail='company ith this name already registered'
        )

    return {'id': str(company.inserted_id), **data.dict()}

@router.get('/', response_model=List[CompanySchema])
async def list_companies(name: str = None, auth: Autheticate = Depends()):
    filters = {}

    # If name filter, apply it
    if name:
        # We will work just withexact match for now
        filters['name'] = name

    companies = db.companies.find(filters)

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

@router.patch('/{id}/')
async def update_company(id: str, data: UpdateCompanySchema, auth: IsAdmin = Depends()):
    try:
        # Update company data in db
        result = db.companies.update_one(
            {'_id': ObjectId(id)},
            {'$set': data.dict(exclude_unset=True)}
        )
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='invalid id')
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail='name already registered')
    except errors.WriteError:
        raise HTTPException(status_code=400, detail='nothing to update')

    if result.matched_count <= 0:
        raise HTTPException(status_code=404, detail='company not found')

    return Response(status_code=204)

@router.delete('/{id}/')
async def delete_user(id: str, auth: IsAdmin = Depends()):
    # Remove references to this company
    result = db.users.update_many({'company_id': id}, {'$set': {'company_id': None}})
    
    try:
        # delete company data in db
        result = db.companies.delete_one({'_id': ObjectId(id)})
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail='invalid id')

    if result.deleted_count <= 0:
        raise HTTPException(status_code=404, detail='company not found')

    return Response(status_code=204)

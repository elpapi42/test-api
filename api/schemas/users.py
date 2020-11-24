from typing import Optional
from enum import Enum

from bson.objectid import ObjectId
from pydantic import BaseModel, validator, ValidationError
from validator_collection import checkers

from api.database import db


class UserGender(str, Enum):
    male = 'M'
    female = 'F'

class ProfileSchema(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    gender: Optional[UserGender]
    document_number: Optional[str]

    @validator('age')
    def validate_age(cls, v):
        if v <= 0 or v >= 100:
            raise TypeError('invalid age')
        return v

class UserValidatorsModel(BaseModel):
    """Packs the validation to the input of users models."""
    @validator('email', check_fields=False)
    def validate_email(cls, v):
        if not checkers.is_email(v):
            raise TypeError('invalid email')
        return v
    
    @validator('company_id', check_fields=False)
    def validate_company_id(cls, v):
        """Check the supplied company exist in db."""
        count = db.companies.count_documents({'_id': ObjectId(v)})
        if count < 1:
            raise TypeError('supplied company is not registered')
        return v

class UserSchema(BaseModel):
    id: str
    email: str
    company_id: Optional[str]
    profile: Optional[ProfileSchema]
    admin: Optional[bool] = False

class CreateUserSchema(UserValidatorsModel):
    email: str
    password: str
    company_id: Optional[str] = None
    profile: Optional[ProfileSchema]

class UpdateUserSchema(UserValidatorsModel):
    password: Optional[str]
    company_id: Optional[str]
    profile: Optional[ProfileSchema]
    admin: Optional[bool]

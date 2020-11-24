from typing import Optional
from enum import Enum

from pydantic import BaseModel


class UserGender(str, Enum):
    male = 'M'
    female = 'F'

class ProfileSchema(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    gender: Optional[UserGender]
    document_number: Optional[str]

class UserSchema(BaseModel):
    id: str
    email: str
    company_id: Optional[str]
    profile: Optional[ProfileSchema]
    admin: Optional[bool] = False

class CreateUserSchema(BaseModel):
    email: str
    password: str
    company_id: Optional[str] = None
    profile: Optional[ProfileSchema]

class UpdateUserSchema(BaseModel):
    password: Optional[str]
    company_id: Optional[str]
    profile: Optional[ProfileSchema]
    admin: Optional[bool]

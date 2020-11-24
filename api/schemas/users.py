from typing import Optional

from pydantic import BaseModel


class ProfileSchema(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
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

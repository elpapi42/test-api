from typing import Optional

from pydantic import BaseModel


class ProfileSchema(BaseModel):
    name: str
    last_name: str
    age: int
    gender: str
    document_number: str

class UserSchema(BaseModel):
    email: str
    company_id: str
    profile: ProfileSchema

class CreateUserSchema(UserSchema):
    password: str

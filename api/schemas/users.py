from typing import Optional

from pydantic import BaseModel


class ProfileSchema(BaseModel):
    name: str
    last_name: str
    age: int
    gender: str
    document_number: str

class UpdateUserSchema(BaseModel):
    company_id: str
    profile: ProfileSchema

class UserSchema(UpdateUserSchema):
    email: str

class CreateUserSchema(UserSchema):
    password: str

class RetrieveUserSchema(UserSchema):
    id: str

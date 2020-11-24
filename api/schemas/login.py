from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str

class TokenSchema(BaseModel):
    token: str
    token_type: str
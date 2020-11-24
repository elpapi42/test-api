from typing import Optional

from pydantic import BaseModel


class CompanySchema(BaseModel):
    id: str
    name: str
    nit: str
    address: str

class CreateCompanySchema(BaseModel):
    name: str
    nit: str
    address: str

class UpdateCompanySchema(BaseModel):
    name: Optional[str]
    nit: Optional[str]
    address: Optional[str]

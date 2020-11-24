from typing import Optional

from pydantic import BaseModel


class CompanySchema(BaseModel):
    id: str
    name: str
    nit: str
    address: str

class WriteCompanySchema(BaseModel):
    name: str
    nit: str
    address: str

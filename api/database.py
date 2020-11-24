from pymongo import MongoClient, ASCENDING

from api import settings


client = MongoClient(settings.DB_URL)

db = client[settings.DB_NAME]

def setup():
    """Setup database stuff, like indexes."""

    # An index for ensure users email is unique
    db.users.create_index([('email', ASCENDING)], unique=True)
    db.users.create_index([('company_id', ASCENDING)])

    # An index for ensure companies name is unique
    db.companies.create_index([('name', ASCENDING)], unique=True)

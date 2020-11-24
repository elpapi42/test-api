from typing import List

from fastapi import APIRouter, Depends, Query

from api.database import db
from api.schemas.users import UserGender
from api.auth import IsAdmin


router = APIRouter()

@router.get('/')
async def users_stats(
    gender: List[UserGender] = Query(['M', 'F']),
    age: List[int] = Query([19, 20, 21, 22, 23]),
    auth: IsAdmin = Depends()
):
    """Returns statistics about registered users."""
    stats = {}

    for g in gender:
        for a in age:
            stats[f'{g}:{a}'] = db.users.count_documents({'profile.gender': g, 'profile.age': a})

    return stats

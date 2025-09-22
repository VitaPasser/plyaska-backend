from typing import List

from fastapi import HTTPException

from src.models.User import User
from src.utils.controllers.CrudRouter import CRUDRouter

crud_router = CRUDRouter[User, User, User](
    model=User,
    exclude=[CRUDRouter.find_all.__name__]
)

router = crud_router.router


@router.get('/', response_model=List[User] | User)
async def find_by_username(username: str | None = None):
    if username is not None:
        user = await User.find_one(User.username == username)
        if not user:
            raise HTTPException(status_code=404, detail="Not found")
        return user
    return await crud_router.find_all()

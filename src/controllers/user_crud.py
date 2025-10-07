from fastapi import HTTPException

from src import repositories
from src.models.user import User
from src.utils.controllers.crud_router import CRUDRouter
from src.utils.models.create_update_dto_maker import make_create_schema

crud_router = CRUDRouter(model=User, exclude=[CRUDRouter.find_all.__name__, "create"])

router = crud_router.router


@router.get("/", response_model=list[User] | User)
async def find_by_username(username: str | None = None):
    if username is not None:
        user = await User.find_one(User.username == username)
        if not user:
            raise HTTPException(status_code=404, detail="Not found")
        return user
    return await repositories.user.find_all()


@router.post("/", response_model=User, status_code=201)
async def create(user: make_create_schema(User)):
    return await repositories.user.create(user)

from src.models.promotion import Promotion
from src.utils.controllers.crud_router import CRUDRouter

router = CRUDRouter(model=Promotion).router

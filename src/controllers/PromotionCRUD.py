from src.models.Promotion import Promotion
from src.utils.controllers.CrudRouter import CRUDRouter

router = CRUDRouter(model=Promotion).router

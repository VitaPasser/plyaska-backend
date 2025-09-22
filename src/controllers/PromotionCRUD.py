from src.models.Promotion import Promotion
from src.utils.controllers.AutoCRUD import CRUDRouter

router = CRUDRouter(model=Promotion).router

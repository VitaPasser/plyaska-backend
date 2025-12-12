from fastapi import APIRouter
from starlette_prometheus import metrics

router = APIRouter(prefix='/metrics', tags=["Utils"])
router.get('/')(metrics)
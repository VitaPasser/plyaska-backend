from fastapi import APIRouter

router = APIRouter(prefix='/healthcheck',tags=['Utils'])

@router.get('/')
def healthcheck():
    return "It's work."
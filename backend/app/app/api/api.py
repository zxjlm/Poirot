from fastapi import APIRouter

from app.api.api_v1.endpoints import utils

api_router = APIRouter()
api_router.include_router(utils.main_api_router, prefix="/api", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])

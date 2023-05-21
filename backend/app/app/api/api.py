from fastapi import APIRouter

from app.api.api_v1.endpoints.font import font_api_router

api_router = APIRouter()
api_router.include_router(font_api_router, prefix="/api", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])

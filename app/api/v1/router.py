from fastapi import APIRouter

from .endpoints import upload, files, auth

router = APIRouter(prefix="/v1")
router.include_router(upload.router, tags=["Upload"])
router.include_router(files.router, tags=["Files"])
router.include_router(auth.router, tags=["Auth"])
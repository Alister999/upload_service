from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.database import init_db, db_config
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Upload Service",
    description="A service for uploading and managing files",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# # Настройка CORS (если API используется фронтендом)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.CORS_ORIGINS,  # Например, ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.include_router(v1_router, prefix="/api")

# # Обработка ошибок
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     logger.error(f"Validation error: {exc.errors()}")
#     return JSONResponse(
#         status_code=422,
#         content={"detail": exc.errors()}
#     )

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     logger.error(f"HTTP error: {exc.detail}")
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail}
#     )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={f"detail": "Internal server error"}
    )


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")
    await init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")
    await db_config.get_engine().dispose()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
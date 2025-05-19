from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import router

app = FastAPI(
    title=" App API",
    description="API для работы с бд new",
    version="1.0.0"
)


app.include_router(router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    return {"message": "API is running!"}
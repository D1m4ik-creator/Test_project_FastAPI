from fastapi import FastAPI
from fastapi import APIRouter
from api.handlers import user_router
import uvicorn
import uuid


app = FastAPI(title="Тестовое приложение", description="Приложение для изучения FastAPI и SQLAlchemy", version="1.0.0")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/users", tags=["Пользователи"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
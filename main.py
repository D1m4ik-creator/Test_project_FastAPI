from fastapi import FastAPI
from .routers import tasks  # Импортируем наш роутер задач

app = FastAPI()

fake_database =[{"id": 1, "title": "Задача 1"}, {"id": 2, "title": "Задача 2"}]

app = FastAPI(
    title="Мой супер To-Do API",
    description="API для управления задачами, написанное по статье с Хабра",
    version="1.0.0"
)

# Подключаем роутер к главному приложению
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Добро пожаловать в API! Перейдите на /docs для документации."}
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, EmailStr
from pydantic import validator
from fastapi import HTTPException, APIRouter
import settings
import re
import uuid
import uvicorn


"""Блок для работы с базой данных"""

engine = create_async_engine(settings.REAL_DATABASE_URL, echo=True, future=True)

# объект сессии асинхронного взаимодействия с базой данных

assync_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Взаимодействие с базой данных

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)


# Бизес логика связанная с пользователями
class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(name=name, surname=surname, email=email)
        self.db_session.add(new_user)
        await self.db_session.flush()  # Обновляем объект new_user с данными из базы данных
        return new_user


LETTER_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
# Блок для с запросами от пользователя
class TunedModel(BaseModel):
    class Config:
        # Будет переводить в json все что получает
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: str
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr


    @validator('name')
    def validate(cls, value):
        if not LETTER_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Имя должно содержать только буквы")
        return value
    
    @validator('surname')
    def validate(cls, value):
        if not LETTER_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Фамилия должна содержать только буквы")
        return value
    
# Блок для работы с роутами API

app = FastAPI(title="Тестовое приложение", description="Приложение для изучения FastAPI и SQLAlchemy", version="1.0.0")

user_router = APIRouter()


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with assync_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name, 
                surname=body.surname, 
                email=body.email
                )
            return ShowUser(user_id=user.user_id, 
                            name=user.name, 
                            surname=user.surname, 
                            email=user.email, 
                            is_active=user.is_active)


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/users", tags=["Пользователи"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
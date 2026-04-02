
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User

# Бизес логика связанная с пользователями
class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(name=name, surname=surname, email=email)
        self.db_session.add(new_user)
        await self.db_session.flush()  # Обновляем объект new_user с данными из базы данных
        return new_user
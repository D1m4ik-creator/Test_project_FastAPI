# Это файл будет использоваться для сериализация и десирализации данных, которые мы будем получать от пользователя и отправлять ему в ответ
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

import uuid
import re


LETTER_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


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


    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not LETTER_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Имя должно содержать только буквы")
        return value

    @field_validator("surname")
    def validate_surname(cls, value: str) -> str:
        if not LETTER_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Фамилия должна содержать только буквы")
        return value

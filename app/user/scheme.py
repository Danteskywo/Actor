from sqlalchemy.ext.asyncio import AsyncSession  #Асинхронная сессия БД
from sqlalchemy import select, update, delete # SQL операции
from sqlalchemy.orm import selectinload # Загрузка связей

from typing import List, Optional # Аннотации типов
# List - элементов определенного типа
# Optional - значение может быть указанного типа или None
# Dict (словарь) с указанием типов ключей и значений
# Tuple с фиксированным количеством элементов и их типами
# Set (множество) элементов определенного типа
# Any - значение любого типа

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date

from .models import User # SQLAlchemy модели
from .scheme import UserCreate, UserUpdate, UserResponse # Pydantic схемы


class UserRegister(BaseModel):
    username: str = Field(default=..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(default=..., min_length=6)
    first_name: str = Field(default=..., min_length=3)
    last_name: str = Field(default=..., min_length=3)
    date_birth: date

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


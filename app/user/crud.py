from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional
from datetime import datetime
import bcrypt

from .models import User
from .scheme import UserRegister


class UserCRUD:
    async def create_user(self, session: AsyncSession, user_data: UserRegister) -> User:
        # Проверка на уникальность Email и username! 
        existing = await session.execute(select(User).where(
            (User.username == user_data.username)|(User.email == user_data.email)
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError("Пользователь с таким Именем или Email уже существует!")
        
        # Хэшируем пароль

        hashed_password = bcrypt.hashpw(
            user_data.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        # Создаем пользователя!
        user = User(
            username=user_data.username,
            email= user_data.email,
            hashed_password = hashed_password,
            first_name = user_data.first_name,
            last_name = user_data.last_name,
            date_birth = user_data.date_birth,
            is_active = True,
            is_verified=False
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def authenticate_user(self, session: AsyncSession, username: str, password: str) -> Optional[User]:
        result = await session.execute(
            select(User).where(
                (User.username == username)|
                (User.email == username)
            )
        )
        user = result.scalar_one_or_none()

        if not user:
            return None
        if not user.is_active:
            return None
        
        

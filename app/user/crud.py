from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.user.models import User
from app.user.scheme import UserRegister
import hashlib

class UserCRUD:
    @staticmethod
    def get_password_hash(password: str) -> str:
        # Используем SHA256 для хеширования паролей вместо bcrypt
        # Это решит проблему с ограничением длины и проблемой с bcrypt.__about__
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Проверяем пароль через SHA256
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
    
    async def create_user(self, session: AsyncSession, user_data: UserRegister) -> User:
        # Проверяем существование пользователя по username
        stmt = select(User).where(User.username == user_data.username)
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            raise ValueError("Пользователь с таким именем уже существует")
        
        # Проверяем существование пользователя по email
        stmt = select(User).where(User.email == user_data.email)
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            raise ValueError("Пользователь с таким email уже существует")
        
        # Проверяем длину пароля
        if len(user_data.password) > 100:
            raise ValueError("Пароль слишком длинный (максимум 100 символов)")
        
        if len(user_data.password) < 6:
            raise ValueError("Пароль слишком короткий (минимум 6 символов)")
        
        # Создаем пользователя
        hashed_password = self.get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    @staticmethod
    async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[User]:
        # Сначала ищем по username
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            # Если не нашли по username, пробуем по email
            stmt = select(User).where(User.email == username)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        # Проверяем пароль с использованием SHA256
        if not UserCRUD.verify_password(password, user.hashed_password):
            return None
        
        return user
    
    async def get_user_by_username(self, session: AsyncSession, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

user_crud = UserCRUD()
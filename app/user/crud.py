from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from app.user.models import User
from app.user.scheme import UserRegister

class UserCRUD:
    async def create_user(self, session: AsyncSession, user_data: UserRegister) -> User:
        result = await session.execute(
            select(User).where(
                (User.username == user_data.username) |
                (User.email == user_data.email)
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise ValueError("Пользователь уже существует!")
        
        hashed_password = bcrypt.hashpw(
            user_data.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> User:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def authenticate_user(session: AsyncSession, username: str, password: str) -> User:
        user = await UserCRUD.get_user_by_username(session, username)
        if not user:
            print(f"Пользователь {username} не найден!")
            return None
        if not user.is_active:
            print(f"Пользователь {username} неактивен!")
            return None
        if not user.check_password(password):
            print(f"Неверный пароль для пользователя! {username}")
            return None
        return user
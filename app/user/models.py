# app/user/models.py
from sqlalchemy import String, Boolean, Enum, ForeignKey, Text, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import Optional, List
from datetime import datetime, date

# Импортируем аннотации из вашей database.py
from app.database import Base, int_pk, str_uniq, str_null_true, created_at, updated_at


class UserRole(str, enum.Enum):
    """Роли пользователей в системе"""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):
    """Модель пользователя с авторизацией"""
    __tablename__ = "users"
    
    # Основные поля (из вашей схемы)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[str_uniq] = mapped_column(String(255))
    
    # Поля для аутентификации (добавляем)
    username: Mapped[str_uniq] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Дополнительные поля профиля
    avatar_url: Mapped[str_null_true] = mapped_column(String(500))
    phone: Mapped[str_null_true] = mapped_column(String(20))
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Статусы и роли
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )
    
    # Временные метки
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Наследуем базовые поля из Base
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    # Связи
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Если у вас есть связь с актерами, можно добавить:
    # actors: Mapped[List["Actor"]] = relationship(back_populates="user")
    
    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r}, "
                f"last_name={self.last_name!r}, "
                f"email={self.email!r})")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"
    
    @property
    def full_name(self) -> str:
        """Полное имя пользователя"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self) -> bool:
        """Проверка, является ли пользователь администратором"""
        return self.role == UserRole.ADMIN
    
    @property
    def is_moderator(self) -> bool:
        """Проверка, является ли пользователь модератором"""
        return self.role == UserRole.MODERATOR


class RefreshToken(Base):
    """Модель для хранения refresh токенов"""
    __tablename__ = "refresh_tokens"
    
    token: Mapped[str_uniq] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_agent: Mapped[str_null_true] = mapped_column(String(500))
    ip_address: Mapped[str_null_true] = mapped_column(String(50))
    
    # Базовые поля
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    
    # Связи
    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"RefreshToken(id={self.id}, user_id={self.user_id})"
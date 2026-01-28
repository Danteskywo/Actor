from datetime import datetime, timedelta
#  timedelta - разницы между датами или длительности
from typing import Optional
# Аннотация типов
from jose import jwt
# для безопасной передачи информации в виде JSON-объекта
from fastapi import HTTPException, status, Depends
# для обработки ошибок и зависимостей.
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# HTTPBearer - схема безопасности для Bearer токенов
# HTTPAuthorizationCredentials - объект с данными авторизации
import os

SECRET_KEY = 54321 # Ключ для подписи токенов
ALGORITHM = "HS256" # Алгоритм шифрования
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Срок жизни токена 

security = HTTPBearer() # Для извлечения токена из заголовка

class AuthHandler:
    # Создаем токен! 
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    # Проверка текущего пользователя, токен
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        token = credentials.credentials # Берем токен из заголовка
        payload = AuthHandler.verify_token(token) # Проверяем токен
        return {
            "user_id": int (payload.get("sub")),
            "username" : payload.get("username"),
            "is_superuser" : payload.get("is_superuser", False)
        }

auth_handler = AuthHandler()
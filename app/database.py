from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Формат строки подключения: postgresql://<пользователь>:<пароль>@<адрес_сервера>/<имя_базы_данных>
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:77777@localhost:5433/ActorBD"
# Создаем движок (engine)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Создаем фабрику сессий для работы с базой
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Базовый класс для объявления ваших моделей (таблиц БД)
Base = declarative_base()

# Функция для получения сессии БД в маршрутах FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
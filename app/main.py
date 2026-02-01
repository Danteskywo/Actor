
from fastapi import FastAPI, Depends, HTTPException, Query
# Импорт основных инструментов FastAPI для создания веб-приложения.
# Depends - Зависимости/ Внедрение зависимостей
# HTTPException - Ошибки API, cпециальное исключение для HTTP ошибок,
# автоматически конвертируется в JSON ответ,
# Позволяет задать статус код и сообщение
# Query - Параметры запроса, Ограничения (min/max, регулярные выражения)
# Значения по умолчанию, Валидация параметров URL

from sqlalchemy.ext.asyncio import AsyncSession
# Асинхронная сессия для работы с БД в FastAPI.
# Позволяет выполнять SQL-запросы не блокируя основной поток.

from typing import List, Optional
# Аннотации типов для Python. Какие типы данных ожидаются в вашем коде?
# List - Список определённого типа
# Optional - Может быть указанного типа или None

from contextlib import asynccontextmanager
# Декоратор для создания асинхронных контекстных менеджеров.
# Позволяет создавать собственные async with блоки с настройкой и очисткой ресурсов.


from fastapi.middleware.cors import CORSMiddleware
# Промежуточное ПО для разрешения CORS (Cross-Origin Resource Sharing).
# Позволяет вашему FastAPI API принимать запросы с других доменов
#  (например, с фронтенда на React).


from app.database import Base, get_async_session, engine
# Импорт компонентов базы данных для работы с
# PostgreSQL через SQLAlchemy в FastAPI проекте Actor.
# Base - Базовый класс для моделей
# get_async_session - Фабрика асинхронных сессий
# engine - Движок подключения к БД

from app.actors.scheme import ActorCreate, ActorResponse, ActorUpdate, SpecialCreate, SpecialResponse
# Импорт Pydantic схем для валидации,
# сериализации и документирования данных актеров и специализаций в FastAPI.
# Формы ответа: SpecialResponse Схема для ответа со специализацией,
 
from app.actors.crud import actor_crud, special_crud
# Импорт CRUD операций для работы с актерами и специализациями в базе данных.
# CRUD = Create, Read, Update, Delete.


from app.user.scheme import UserRegister, UserLogin, UserResponse, TokenResponse
# Импорт Pydantic схем для системы аутентификации
#  и пользователей в FastAPI проекте Actor.

from app.user.crud import UserCRUD
# Импорт класса CRUD операций для пользователей
# — содержит всю логику работы с пользователями в базе данных
# (создание, аутентификация, обновление, удаление).


from app.user.auth import auth_handler
# Импорт обработчика аутентификации — утилита для работы с JWT токенами
# (создание, валидация, обновление) в вашем FastAPI проекте Actor.
# Создаёт JWT токены, Проверяет валидность токенов, Декодирует данные из токенов,
# Управляет сроком жизни токенов, Обрабатывает refresh токены

from fastapi.security import HTTPBearer
# Схема безопасности для HTTP Bearer аутентификации через заголовок Authorization.
# Это стандартный способ передачи JWT токенов в HTTP запросах.
# Bearer Authentication (аутентификация предъявителя) ->
# Стандартный способ передачи токенов в HTTP
# Автоматическая валидация формата заголовка
# Интеграция с Swagger документацией
# Извлечение токена из запроса

from fastapi.staticfiles import StaticFiles
# Импортирование наших статических файлов

import os
# Импорт стандартного модуля Python для работы с операционной системой.
# Позволяет взаимодействовать с файловой системой,
# переменными окружения, путями и другими системными функциями.

########################################################################################

# Паттерн - это типовое, проверенное временем решение часто возникающей 
# проблемы проектирования программного обеспечения. Это не готовая реализация, 
# а шаблон (рецепт), который можно адаптировать под конкретную задачу.

# FastAPI - класс конструктор, представляющий ядро веб-фреймворка. 
# Это точка входа для создания экземпляра приложения, который 
# регистрирует маршруты, middleware, обработчиков исключений и
# предоставляет ASGI(Асинхронный Интерфейс Шлюза Сервера)-
# совместимый интерфейс для запуска сервера.
# Примером из жизни может служить главный офис компании.
# Допустим вы начинаете строительство бизнеса с создания офиса
# ( app = FastAPI() ), куда будут приходить запросы(клиенты/письма),
# распределяться по отделам (маршрутам) и формироваться ответы.

# HTTPException - класс-исключение для явного возврата HTTP-ответов с 
# ненулевым(нулевыми считаются статус коды 2хх, то успешные статус коды 
# считаются нулевыми. 1хх считаются информационными, 3хх считаются 
# перенаправления в особых случаях, 4хх это статус коды ошибок клиента, 
# 5хх - это статус коды серьезных ошибок сервера) статус-кодом и 
# деталями ошибки в структурированном виде. Наследуется от Exception.
# Примером из жизни можно привести официальный письменные отказ от 
# банка на выдачу кредита. Вместо того чтобы просто не ответить, 
# банк отправляет документ с кодом отказа(статус 400), заголовком 
# "Недостаточно данных" и описанием "Не предоставлена справка о доходах".

# Query - класс-зависимость (на англ. Dependency переводится как зависимость),
# используемый для извлечения, валидации и документирования параметров строки 
# запроса (query parameters) из URL. Преобразует строковые данные запроса в 
# типизированные значения Python.
# Примером из жини может служить интернет-магазин, когда на сайте магазина 
# выбираете "цена: до 10000", "бренд: Apple", "цвет: черный" - это параметры 
# запроса ?max_price=10000&brand=Apple&color=black .
# Query помогает извлечь и проверить эти параметры.

# Depends - функция/класс для декларативного(желаемый результат) указания 
# зависимостей в FastAPI. Внедряет (инжектирует) результаты выполнения 
# зависимых функций в обработчики маршрутов. Основана на системе внедрения 
# зависимостей (Dependency Injection).
# Примером из жизни можно привести процесс заказа в ресторане. Чтобы подать 
# блюдо(обработать запрос), официанту (обработчику маршрута) нужны: 
# 1) чистый пол (clean_table то есть чистая таблица), 
# 2) готовое блюдо ( prepare_food то есть подготовленная пища), 3) приборы 
# ( get_cultery то есть получить столовые приборы). Depends гарантирует, 
# что эти зависимости будут выполнены перед подачей блюда. 
# Если стол грязный - его сначала моют.

# AsyncSession - класс-фасад( это взаимодействие между пользователем и 
# сложной внутренней системой ) для асинхронного взаимодействия с базой данных.
# Представляет сессию - область взаимодействия (unit of work), которая 
# отслеживает изменения объектов, формирует и выполняет SQL-запросы асинхронно, 
# управляет транзакциями. Является асинхронным аналогом классической Session.
# Примером из жизни может служить сотрудник большого склада. Вы даете ему 
# задание(асинхронный запрос): "Принеси товар ID 777". Он уходит на склад (БД),
# и пока он ищет, вы можете заниматься другими делами(обрабатывать другие запросы). 
# Он вернется с результатом (или ошибкой), когда выполнит задание.

# engine - объект-фабрика(производит соединения, скрывая сложность создания) 
# пулов(пул - кэш готовых соеднинений для эффективного повторного использования) 
# соединений (с англ. connection pool) и диалекта SQL. Инкапсулирует информацию 
# о подключении к БД (URL, драйвер, настройки), управляет жизненным циклом соединений.
# В асинхронном режиме использует адаптер( это асинхроновые драйвера баз данных для 
# Python, это библиотека, которая обеспечивает связь между приложением на Python и 
# СУБД. Он переводит команды Python в язык, понятный БД. ) asyncpg или aiomysql.
# Примером из жизни может служить центральный офис логистики (диспетчерская такси). 
# У него есть: 
# База данных водителей (пул соединений).
# Знание правил дорог конкретного города (диалект SQL для PostgreSQL/MySQL).
# При поступлении заказа (запроса к БД) диспетчерская находит свободного 
# водителя (соединение) и направляет его на вызов.

# Base - декларативный базовый класс (declarative base). Это метакласс(класс для классов), 
# который связывает Python-классы с таблицами базы данных, создавая модели (ORM-модели 
# они переводят пайтон объекты в таблицу БД, либо так же но наоборот). Хранит 
# метаданные о всех таблицах ( Base.metadata ).
# Пример из жизни - это архитектурный шаблон (ГОСТ) для чертежей зданий. Все архитекторы 
# в компании используют единый стандартный бланк (Base), чтобы создавать чертежи квартир 
# (Actor). Это гарантирует, что все чертежи совместимы и из них 
# можно собрать общий план дома (Base.metadata).

# typing - модуль стандартной библиотека Python, предоставляющий поддержку подсказок типов 
# (type hints). Содержит специальные конструкции для аннотаций типов коллекций опциональных 
# значений, вызываемых объектов и других сложных типов.

# list - универсальный тип Generic указывающий, что переменная или параметр 
# является списком, содержащим элементы определенного типа.

# Optional - универсальный тип, указывающий что значение может быть либо указанного типа либо None. 

# contextlib -модуль стандартной библиотеки Python, содержащий утилиты для работы с контекстными 
# менеджерами. Контекстные менеджеры обеспечивают корректное выделение и освобождение ресурсов.

# asynccontextmanager - декоратор из contextlib, декоратор превращающий асинхронную генераторную 
# функцию в асинхронный контекстный менеджер. Позволяет создавать собественные менеджеры контекста 
# для асинхронного кода.

# asyncio модуль - библиотека для написания параллельного кода с использованием синтекса async/await.
# Предоставляет event loop, задачи, футуры и другие примитивы для асинхронного программирования.

# CORSMiddlevare - это промежуточное программное обеспечение для обработки механизма 
# CORS(Cross-Origin Resource Sharing) - это обмен ресурсами между разными источниками. 
# Разрешает или запрещает кросс-доменные запросы от браузеров.

# from fastapi.templating import Jinja2Templates  ##
# from fastapi.responses import HTMLResponse
################################################################################################################################

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("База данных инициализирована!")
    yield
    print("Приложение останавливается...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def home():
    return {"message": "API запущено"}

@app.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, session: AsyncSession = Depends(get_async_session)):
    crud = UserCRUD()
    try:
        user = await crud.create_user(session, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_async_session)):
    user = await UserCRUD.authenticate_user(session, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неверные имя пользователя или пароль")
    access_token = auth_handler.create_access_token(data={"sub": str(user.id), "username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
async def get_current_user(user: dict = Depends(auth_handler.get_current_user), session: AsyncSession = Depends(get_async_session)):
    crud = UserCRUD()
    db_user = await crud.get_user_by_username(session, user["username"])
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user

@app.options("/actors/")
async def options_actors():
    return {}

@app.post("/actors/", response_model=ActorResponse)
async def create_actor(
    actor_data: ActorCreate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        actor = await actor_crud.create(session, actor_data)
        return actor
    except Exception as e: 
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/actors/", response_model=List[ActorResponse])
async def get_all_actors(
    oscar_wins: Optional[int] = Query(None, description="Фильтр по количеству оскаров"),
    session: AsyncSession = Depends(get_async_session)
):
    actors = await actor_crud.get_all(session)
    if oscar_wins is not None:
        actors = [actor for actor in actors if actor.oscar_wins == oscar_wins]
    return actors

@app.get("/actors/{actor_id}", response_model=ActorResponse)
async def get_actor_by_id(
    actor_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    actor = await actor_crud.get_by_id(session, actor_id)
    if not actor: 
        raise HTTPException(status_code=404, detail=f"Актер с ID {actor_id} не найден")
    return actor

@app.put("/actors/{actor_id}", response_model=ActorResponse)
async def update_actor(
    actor_id: int,
    actor_data: ActorUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    actor = await actor_crud.update(session, actor_id, actor_data)
    if not actor:
        raise HTTPException(status_code=404, detail=f"Актер с ID {actor_id} не найден")
    return actor

@app.delete("/actors/{actor_id}")
async def delete_actor(
    actor_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    success = await actor_crud.delete(session, actor_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Актер с ID {actor_id} не найден")
    return {"message": f"Актер с ID {actor_id} успешно удален!"}

@app.get("/actors/search/", response_model=List[ActorResponse])
async def search_actors(
    name: str = Query(default=..., description="Поиск актера по имени и фамилии"),
    session: AsyncSession = Depends(get_async_session)
):
    actors = await actor_crud.search(session, name)
    return actors

@app.get("/specials/", response_model=List[SpecialResponse])
async def get_all_specials(session: AsyncSession = Depends(get_async_session)):
    specials = await special_crud.get_all(session)
    return specials

@app.get("/specials/{special_id}", response_model=SpecialResponse)
async def get_special_by_id(
    special_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    special = await special_crud.get_by_id(session, special_id)
    if not special:
        raise HTTPException(status_code=404, detail=f"Специализация с ID {special_id} не найдена")
    return special

@app.post("/specials/", response_model=SpecialResponse)
async def create_special(
    special_data: SpecialCreate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        special = await special_crud.create(session, special_data)
        return special
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/specials/{special_id}", response_model=SpecialResponse)
async def update_special(
    special_id: int,
    special_data: SpecialCreate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        special = await special_crud.get_by_id(session, special_id)
        if not special:
            raise HTTPException(status_code=404, detail=f"Специализация с ID {special_id} не найдена")
        
        update_data = special_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(special, key, value)
        
        await session.commit()
        await session.refresh(special)
        return special
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/specials/{special_id}")
async def delete_special(
    special_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    success = await special_crud.delete(session, special_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Специализация с ID {special_id} не найдена")
    return {"message": f"Специализация с ID {special_id} успешно удалена!"}

static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    print(f"Статические файлы подключены из: {static_dir}")
else:
    print(f"Папка static не найдена: {static_dir}")
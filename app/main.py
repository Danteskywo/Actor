from fastapi import FastAPI, HTTPException, Query, Depends 

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

# 

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from app.actors.models import Actor, Special
from app.database import engine, get_async_session, Base
from app.actors.scheme import ActorCreate, ActorResponse, ActorUpdate, SpecialCreate, SpecialResponse
from app.actors.crud import actor_crud, special_crud

from fastapi.staticfiles import StaticFiles


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы!")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База данных успешно создана, Повелитель!")
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
    return {"message": "API запущенно"}


@app.options("/actors/")
async def options_actors():
    return {}


@app.post("/post/actors/", response_model=ActorResponse)
async def create_actor(
    actor_data:ActorCreate,
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
        raise HTTPException(status_code=404, detail=f"Ошибка!{actor_id}Такой ID не найден")
    return actor

@app.put("/actors/{actor_id}", response_model=ActorResponse)
async def update_actor(
    actor_id:int,
    actor_data: ActorUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    actor = await actor_crud.update(session, actor_id, actor_data)
    if not actor:
        raise HTTPException(status_code=404, detail=f"Ошибка!{actor_id}Такой ID не найден в обновлении!")
    return actor

@app.delete("/actors/{actor_id}")
async def delete_actor(
    actor_id:int,
    session: AsyncSession = Depends(get_async_session)
):
    success = await actor_crud.delete(session, actor_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Актер с таким ID {actor_id} не найден!")
    return {"message":f"Актер с ID{actor_id} успешно удален!"}

@app.get("/actors/search/")
async def search_actors(
    name: str = Query(default=..., description="Поиск Актера по имени и фамилии"),
    session: AsyncSession = Depends(get_async_session)
):
    actors = await actor_crud.search(session, name)
    return actors

@app.get("/actors/filter/oscar/")
async def filter_actors_by_oscar(
    oscar_wins: int = Query(..., ge=0, description="Количество оскаров"),
    oscar_nominations: Optional[int] = Query(None, ge=0, description="Количество номинаций"),
    session: AsyncSession = Depends(get_async_session)
):
    actors = await actor_crud.get_all(session)

    filtered_actors = []
    for actor in actors:
        if actor.oscar_wins == oscar_wins:
            if oscar_nominations is None or actor.oscar_nominations == oscar_nominations:
                filtered_actors.append(actor)
    return filtered_actors

@app.get("/actors/oscar/{oscar_wins}")
async def get_actors_by_oscar_wins(
    oscar_wins: int,
    session: AsyncSession = Depends(get_async_session)
    ):
    actors = await actor_crud.get_all(session)

    result_list = []
    for actor in actors:
        if actor.oscar_wins == oscar_wins:
            result_list.append(actor)

    if not result_list:
        raise HTTPException(
            status_code=404,
            detail=f"Актер с таким количеством не найден {oscar_wins}"
        )
    return {
        "oscar_wins":oscar_wins,
        "count": len(result_list),
        "actors": result_list
    }

@app.get("/actor")
async def get_actor_by_query(
    id: int = Query(..., description="ID актера"),
    session: AsyncSession = Depends(get_async_session)
):
    actor = await actor_crud.get_by_id(session, id)
    if not actor:
        raise HTTPException(
            status_code=404,
            detail=f"Актер с ID {id} не найден"
        )
    return actor

@app.get("/actors/id/{actors_id}")
async def get_actor_by_path(
    actor_id: int,
    session: AsyncSession = Depends(get_async_session) 

):
    actor = await actor_crud.get_by_id(session, actor_id)
    if not actor:
        raise HTTPException(
            status_code=404,
            detail=f"Актер с таким ID {actor_id} не найден"
        )
    return actor


########################--Specials--###########


@app.get("/specials/", response_model=SpecialResponse)
async def get_all_specials(session: AsyncSession = Depends(get_async_session)):
    specials = await special_crud.get_all(session)
    return specials

@app.post("/specials/", response_model=SpecialResponse)
async def create_cpecial(
    special_data: SpecialCreate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        special = await special_crud.create(session, special_data)
        return special
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
app.mount("/", StaticFiles(directory="static", html=True), name="static")


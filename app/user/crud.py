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

from .models import User # SQLAlchemy модели
from .scheme import UserCreate, UserUpdate, UserResponse # Pydantic схемы


class UserCRUD:
    async def create(self, session: AsyncSession, actor_in: ActorCreate) -> Actor:
        # Создаем актера без специализаций
        # self — экземпляр класса 
        actor_dict = actor_in.model_dump(exclude={"specialty"})
        # model_dump() — это основной метод сериализации в Pydantic
        actor = Actor(**actor_dict)
        # Распаковка словаря в аргументы. actor_dict + actor
        session.add(actor)
        
        # Обязательно flush, чтобы получить ID актера
        await session.flush()
        
        # Добавляем специализации, если есть
        # many-to-many в SQLAlchemy
        if actor_in.specialty:
            # Построение запроса
            stmt = select(Special).where(Special.id.in_(actor_in.specialty))
            # Выполнение запроса
            result = await session.execute(stmt) #.extend() - добавляет несколько объектов к связи
            # Получение результатов
            specialties = result.scalars().all() 
            # result.scalars()- извлекает скалярные значения (объекты Special)
            # Добавление связей к актеру
            actor.specialties.extend(specialties)
        
        await session.commit()
        await session.refresh(actor, ["specialties"])  # Явно загружаем связи
        return actor
        
    async def get_all(self, session: AsyncSession) -> List[Actor]:
        stmt = select(Actor).options(selectinload(Actor.specialties))
        #select() - функция/класс для построения SELECT-запросов
        result = await session.execute(stmt) 
        return result.scalars().all()
    
    async def get_by_id(self, session: AsyncSession, actor_id: int) -> Optional[Actor]:
        stmt = select(Actor).where(Actor.id == actor_id).options(selectinload(Actor.specialties))
        #.where(Actor.id == actor_id) - фильтрация по ID
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
        # scalar_one_or_none() - возвращает один результат или None,
        # Вызывает ошибку, если найдено больше одной записи
    
    async def update(self, session: AsyncSession, actor_id: int, actor_in: ActorUpdate) -> Optional[Actor]:
        actor = await self.get_by_id(session, actor_id)
        if not actor:
            return None
        
        # Обновление базовых полей
        update_data = actor_in.model_dump(exclude_unset=True, exclude={"specialty"})
        # exclude_unset=True - исключает поля, которые не были переданы
        # exclude={"specialty"} - исключает указанные поля
        for key, value in update_data.items():
            if value is not None:
                setattr(actor, key, value)
        
        # Обновление специализации
        if actor_in.specialty is not None:

            actor.specialties.clear()
            # Очищаем текущий список специализаций актера
            if actor_in.specialty:
                stmt = select(Special).where(Special.id.in_(actor_in.specialty))
                # Создаем SQL запрос: выбрать все записи из таблицы Special
                result = await session.execute(stmt)
                specialties = result.scalars().all()
                # извлекает только скалярные значения + получает все результаты в виде списка
                actor.specialties.extend(specialties)
                # Добавляем найденные специализации к актеру
        
        await session.commit()
        await session.refresh(actor, ["specialties"])
        return actor
    
    async def delete(self, session: AsyncSession, actor_id: int) -> bool:
        actor = await self.get_by_id(session, actor_id)
        if not actor:
            return False
        
        await session.delete(actor)
        await session.commit()
        return True
    
    async def search(self, session: AsyncSession, name: str) -> List[Actor]:
        stmt = select(Actor).where(
            (Actor.first_name.ilike(f"%{name}%")) |
            (Actor.last_name.ilike(f"%{name}%"))
        ).options(selectinload(Actor.specialties))
        result = await session.execute(stmt)
        return result.scalars().all()


class SpecialCRUD:
    async def create(self, session: AsyncSession, special_in) -> Special:
        special = Special(**special_in.model_dump())
        # special_in.model_dump() - преобразует Pydantic модель в словарь
        # ** - распаковывает словарь в аргументы конструктора
        session.add(special)
        await session.commit()
        await session.refresh(special)
        return special
    
    async def get_all(self, session: AsyncSession) -> List[Special]:
        stmt = select(Special)
        result = await session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, session: AsyncSession, special_id: int) -> Optional[Special]:
        stmt = select(Special).where(Special.id == special_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
        #scalar_one_or_none() - возвращает один объект или None
        # first() - показать 0 или 1 результат. 
    
    async def delete(self, session: AsyncSession, special_id: int) -> bool:
        special = await self.get_by_id(session, special_id)
        if not special:
            return False
        
        await session.delete(special)
        await session.commit()
        return True


actor_crud = ActorCRUD()
special_crud = SpecialCRUD()
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional

from .models import Actor, Special
from .scheme import ActorCreate, ActorUpdate


class ActorCRUD:
    async def create(self, session: AsyncSession, actor_in: ActorCreate) -> Actor:
        actor_dict = actor_in.model_dump(exclude={"specialty"})
        actor = Actor(**actor_dict)
        
        if actor_in.specialty:
            query = select(Special).where(Special.id.in_(actor_in.specialty))
            result = await session.execute(query)
            specialties = result.scalars().all()
            actor.specialties.extend(specialties)
        
        session.add(actor)
        await session.commit()
        await session.refresh(actor)
        return actor
    
    async def get_all(self, session: AsyncSession) -> List[Actor]:
        query = select(Actor)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, session: AsyncSession, actor_id: int) -> Optional[Actor]:
        query = select(Actor).where(Actor.id == actor_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def update(self, session: AsyncSession, actor_id: int, actor_in: ActorUpdate) -> Optional[Actor]:
        actor = await self.get_by_id(session, actor_id)
        if not actor:
            return None
        
        update_dict = actor_in.model_dump(exclude_unset=True, exclude={"specialty"})
        for key, value in update_dict.items():
            if value is not None:
                setattr(actor, key, value)
        
        if actor_in.specialty is not None:
            actor.specialties.clear()
            if actor_in.specialty:
                query = select(Special).where(Special.id.in_(actor_in.specialty))
                result = await session.execute(query)
                specialties = result.scalars().all()
                actor.specialties.extend(specialties)
        
        await session.commit()
        await session.refresh(actor)
        return actor
    
    async def delete(self, session: AsyncSession, actor_id: int) -> bool:
        actor = await self.get_by_id(session, actor_id)
        if not actor:
            return False
        
        await session.delete(actor)
        await session.commit()
        return True
    
    async def search(self, session: AsyncSession, name: str) -> List[Actor]:
        query = select(Actor).where(
            (Actor.first_name.ilike(f"%{name}%")) |
            (Actor.last_name.ilike(f"%{name}%"))
        )
        result = await session.execute(query)
        return result.scalars().all()

class SpecialCRUD:
    async def create(self, session: AsyncSession, special_in) -> Special:
        special = Special(**special_in.model_dump())
        session.add(special)
        await session.commit()
        await session.refresh(special)
        return special
    
    async def get_all(self, session: AsyncSession) -> List[Special]:
        query = select(Special)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, session: AsyncSession, special_id: int) -> Optional[Special]:
        query = select(Special).where(Special.id == special_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def delete(self, session: AsyncSession, special_id: int) -> bool:
        special = await self.get_by_id(session, special_id)
        if not special:
            return False
        
        await session.delete(special)
        await session.commit()
        return True


actor_crud = ActorCRUD()
special_crud = SpecialCRUD()
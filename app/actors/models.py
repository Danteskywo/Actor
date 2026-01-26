from sqlalchemy import ForeignKey, text, Text, Table, Column
# SQLAlchemy - ORM и типы данных. Table- описание таблицы, Column - опр. колонку таблицы.
from sqlalchemy.orm import relationship, Mapped, mapped_column
# relationship - связывает модели между собой (один-ко-многим, много-ко-многим)
# Mapped - аннотация типов для полей модели (современный стиль SQLAlchemy 2.0)
# mapped_column - замена старого Column() в декларативном стиле


from app.database import Base, str_uniq, int_pk, str_null_true
# Base - родительский класс для всех моделей (база данных)
# str_uniq - строка, которая должна быть уникальной в таблице
# int_pk - целое число, которое будет первичным ключом
# str_null_true - строка, которая может быть пустой (NULL)

from datetime import date
from typing import Optional, List


# Промежуточная таблица Many-to-Many
actor_specialty = Table(
    'actor_specialty',
    Base.metadata,
    Column('actor_id', ForeignKey('actors.id'), primary_key=True),
    Column('special_id', ForeignKey('specials.id'), primary_key=True)    
)

# class ActorSpecialty(Base):
#     ictor_id: Mapped[int] = mapped_column(ForeignKey("actors.id"), primary_key=True)
#     special_id: Mapped[int] = mapped_column(ForeignKey("specials.id"), primary_key=True)

class Actor(Base):
    id: Mapped[int_pk] # Первичный ключ.
    # Mapped — это специальный тип для аннотаций в SQLAlchemy, generic тип
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]
    phone_number: Mapped[str_uniq]
    address: Mapped[str] = mapped_column(Text, nullable=False)
    career_start: Mapped[int] = mapped_column(nullable=True)
    oscar_wins: Mapped[int] = mapped_column(default=0)
    oscar_nominations: Mapped[int] = mapped_column(default=0)
    special_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # special_id: Mapped[int] = mapped_column(ForeignKey("specials.id"), nullable=False)
    specialties: Mapped[List["Special"]] = relationship(  #Many-to-many
        secondary="actor_specialty",
        # secondary - Указывает ассоциативную таблицу для связи многие-ко-многим
        back_populates="actors",
        # Двунаправленная связь - создает зеркальную связь в классе Specialty
        lazy="selectin"
        #Загружает все связанные специальности одним
        #дополнительным запросом после загрузки актеров
    )

    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")  # +!r = 'Robert'

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"
    
class Special (Base):
    id: Mapped[int_pk]
    special_name: Mapped[str_uniq]
    special_description: Mapped[str_null_true]
    count_actor: Mapped [int] = mapped_column(server_default=text('0'))
    actors: Mapped[List["Actor"]] = relationship(
        secondary=actor_specialty,
        back_populates="specialties",
        lazy="selectin"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, special_name={self.special_name!r})"
    def __repr__(self):
        return str(self)
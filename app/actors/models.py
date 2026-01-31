from sqlalchemy import ForeignKey, text, Text, Table, Column, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import date
from typing import Optional, List

actor_specialty = Table(
    'actor_specialty',
    Base.metadata,
    Column('actor_id', ForeignKey('actors.id'), primary_key=True),
    Column('special_id', ForeignKey('specials.id'), primary_key=True)    
)

class Actor(Base):
    __tablename__ = 'actors'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    date_of_birth: Mapped[date]
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    career_start: Mapped[int] = mapped_column(nullable=True)
    oscar_wins: Mapped[int] = mapped_column(default=0)
    oscar_nominations: Mapped[int] = mapped_column(default=0)
    special_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    specialties: Mapped[List["Special"]] = relationship(
        secondary=actor_specialty,
        back_populates="actors",
        lazy="selectin"
    )

    def __repr__(self):
        return f"Actor(id={self.id}, first_name={self.first_name!r}, last_name={self.last_name!r})"

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"
    
class Special(Base):
    __tablename__ = 'specials'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    special_name: Mapped[str] = mapped_column(String(100), unique=True)
    special_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    count_actor: Mapped[int] = mapped_column(server_default=text('0'))
    
    actors: Mapped[List["Actor"]] = relationship(
        secondary=actor_specialty,
        back_populates="specialties",
        lazy="selectin"
    )

    def __str__(self):
        return f"Special(id={self.id}, special_name={self.special_name!r})"
    
    def __repr__(self):
        return str(self)
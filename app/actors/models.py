from sqlalchemy import ForeignKey, text, Text, Table, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date
from typing import Optional, List

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
    id: Mapped[int_pk]
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
    specialties: Mapped[List["Special"]] = relationship(
        secondary="actor_specialty",
        back_populates="actors",
        lazy="selectin"
    )

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")

    def __repr__(self):
        return str(self)
    
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


    



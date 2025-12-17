from enum import Enum, StrEnum, IntEnum
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
from datetime import date, datetime
from typing import Optional, List 
import re


class Specialty(Enum):
    WAR_DRAMAS = (1, "Военная драма")
    SOCIAL_DRAMAS = (2, "Социальная драма")
    THRILLERS = (3, "Триллеры")
    HISTORY_FIGURES = (4,"Исторические личности")
    DRAMATIC_ROLES = (5, "Драматические роли")
    ENVIRONMENTAL_ACTIVISM = (6, "Экологический активизм")
    HISTORICAL_FILMS = (7, "Исторические фильмы")
    ACCENT_MASTERY = (8, "Акцентное мастерство")
    BIOGRAPHICAL_ROLES = (9, "Биографические роли")
    MUSICALS = (10, "Музыкальные роли")
    CLASSICAL_DRAMA = (11, "Классическая драма")
    SUPERHERO_FILMS = (12, "Супергеройские фильмы")
    INDEPENDENT_CINEMA = (13, "Независимое кино")
    SCIENCE_FICTION = (14, "Фантастика")
    FANTASY = (15, "Фэнтези")
    ACTION = (16, "Экшен")
    COMEDIES = (17, "Комедия")

    def __init__(self, id, display_name):
       self.id = id 
       self.display_name = display_name

    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.display_name
    

class SchemActor(BaseModel):
    id: Optional[int] = None
    first_name: str = Field(default=...,min_length=3, max_length=30, description="Имя актера")
    last_name: str = Field(default=..., min_length=3, max_length=30, description="Фамилия актера")
    date_of_birth: date = Field(default=..., description="Дата рождения актера в формате ГГГГ.ММ.ДД")
    email: EmailStr = Field (default=..., description="Электронная почта студента")
    phone_number: str = Field (default=..., description="Номер телефона")
    address: str = Field (default=..., description="Адрес")
    career_start: int = Field (default = ..., ge=1900, le=2025, description="Год начала карьеры")
    oscar_wins: int = Field(default=0, ge=0, description="Количество побед на Оскаре")
    oscar_nominations: int = Field(default=0, ge=0, description="Количество номинаций на Оскар")
    special_notes: Optional[str] = Field(None, description="Особые примечания")
    specialty: List[str] = Field(default=None, description="ID специализаций")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        phone_patten = r'^\+?[\d\s\-\(\)]{7,20}$'
        if not re.match(phone_patten, v):
            raise ValueError("Неправильный номер телефона (пример +9998887766)")
        return v
    
    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, v: date ) -> date:
        if v > date.today():
            raise ValueError ("Дата рождения не может быть в будущем")
        return v
    
    @field_validator("specialty")
    @classmethod
    def validate_specialty(cls, v: Optional[List[int]]) -> Optional[List[int]]:
        if v is not None:
            valid_ids = [spec.id for spec in Specialty]
            for spec_id in v : 
                if spec_id not in valid_ids:
                    raise ValueError(f"ID специальности {spec_id} не существует!")
        return v 
    
            
        
    
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
from datetime import date, datetime
from typing import Optional
import re


class Specialty(int, Enum):
# "Военные драмы": "War dramas",
# "Социальные драмы": "Social dramas", 
# "Триллеры": "Thrillers",
#   "Исторические личности": "Historical figures",
#   "Драматические роли": "Dramatic roles",
#   "Экологические активизм": "Environmental activism",
#   "Исторические фильмы": "Historical films",
#   "Акцентное мастерство": "Accent mastery",
#   "Биографические роли": "Biographical roles",
#   "Мюзиклы": "Musicals",
#   "Классическая драма": "Classical drama",
#   "Супергеройские фильмы": "Superhero films",
#   "Независимое кино": "Independent cinema",
#   "Фантастика": "Science fiction",
#   "Озвучка анимации": "Animation voice acting",
#   "Драмеди": "Dramedy",
#   "Военные фильмы": "War films",
#   "Фильмы-катастрофы": "Disaster films",
#   "Психологические драмы": "Psychological dramas",
#   "Научная фантастика": "Science fiction",
#   "Балетные роли": "Ballet roles",
#   "Фильмы Marvel": "Marvel films",
#   "Продюсирование": "Producing",
#   "Криминальные драмы": "Crime dramas",
#   "Романтические комедии": "Romantic comedies",
#   "Комедии": "Comedies",
#   "Периодные драмы": "Period dramas",
#   "Экшен": "Action",
#   "Фильмы о боевых искусствах": "Martial arts films",
#   "Антигерои": "Antiheroes",
#   "Фэнтези": "Fantasy",
#   "Королевские особы": "Royalty",
#   "Сложные характеры": "Complex characters",

class Actor(BaseModel):
    id: int
    first_name: str = Field(default=...,min_length=3, max_length=30, description="Имя актера")
    last_name: str = Field(default=..., min_length=3, max_length=30, description="Фамилия актера")
    date_of_birth: date = Field(default=..., description="Дата рождения актера в формате ГГГГ.ММ.ДД", )"1969-05-14",
    email: EmailStr = Field (default=..., description="Электронная почта студента")"cate@bluejasmine.com",
    phone_number: "+61-2-555-1010",
    address: "Сидней, Австралия",
    career_start: 1992,
    oscar_wins: 2,
    oscar_nominations: 8,
    special_notes: "Одна из шести актеров, получивших Оскар за роль в фильме на основе комиксов ('Тор: Рагнарёк')",
    specialty: Optional[str] = Field (default=..., ge=1, le=5, description="")["Периодные драмы", "Фэнтези", "Королевские особы", "Сложные характеры"]
  
  
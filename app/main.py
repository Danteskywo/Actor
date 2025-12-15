from fastapi import FastAPI, HTTPException
from utils import json_to_dict_list, dict_list_to_json
import os
from typing import Optional
from fastapi.responses import JSONResponse

# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

#Переходим на уровень выше 

parent_dir = os.path.dirname(script_dir)

#Получаем путь к JSON 

path_to_json = os.path.join(parent_dir,'actors.json')

app = FastAPI()

@app.get("/actors")
def get_all_students(oscar_wins: Optional[int] = None):
    actors = json_to_dict_list(path_to_json)

    if oscar_wins is None:
        return actors
    else:
        return_list = []

        for actor in actors:
            if actor.get("oscar_wins") == oscar_wins:
                return_list.append(actor)
        return return_list

@app.get("/")
def home_page():
    message = {"message":"Привет создатель!"}
    return JSONResponse (content=message)


@app.get("/actors/oscar/{oscar_wins}")
def get_all_oscar_wins(oscar_wins: int):
    actors = json_to_dict_list(path_to_json)
    return_list = []

    for actor in actors:
        if actor["oscar_wins"] == oscar_wins:
            return_list.append(actor)
    if not return_list:
        raise HTTPException(
            status_code=404,
            detail=f"Данное количество оскаровб не найдено {oscar_wins}"
        )
    return {
        "oscar_wins": oscar_wins,
    }

@app.get("/actors/{oscar_wins}")
def get_all_actors_oscar_wins(
    oscar_wins: int,
    oscar_nominations: Optional[int] = None,
    career_start: Optional[int] = None
    ):
    actors = json_to_dict_list(path_to_json)
    filtered_actors = []
    for actor in actors:
        if actor["oscar_wins"] == oscar_wins:
            filtered_actors.append(actor)
    if oscar_nominations:
        filtered_actors = [student for student in filtered_actors if student["oscar_nominations"] == oscar_nominations]
    if career_start:
        filtered_actors = [student for student in filtered_actors if student['career_start'] == career_start]
    
    return filtered_actors
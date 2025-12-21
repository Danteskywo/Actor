from fastapi import FastAPI, HTTPException, Query
from .utils import json_to_dict_list, dict_list_to_json
import os
import models
from typing import Optional, List, Dict, Any
from fastapi.responses import JSONResponse
from app.actors.models import SchemActor


# Создаёт все таблицы, определённые в моделях, если они ещё не существуют
models.Base.metadata.create_all(bind=engine)


# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

#Переходим на уровень выше 

parent_dir = os.path.dirname(script_dir)

#Получаем путь к JSON 

path_to_json = os.path.join(parent_dir,'actors.json')

app = FastAPI(title="База данных по Актерам!")

def get_all_actors():
    return json_to_dict_list(path_to_json)

######### Поиск Актера по ID (параметра запроса!!!) ########

@app.get("/actors/search/")
def get_actor_query(actor_id: int = Query(...,gt=0, description="ID Актера")):
    actors = json_to_dict_list(path_to_json)

    for actor in actors:
        if actor.get("id") == actor_id:
            return actor
    raise HTTPException(
        status_code=404,
        detail=f"Актер с таким ID {actor_id} не нфайден"
        )
######### Поиск Актера по ID (параметра ПУТИ!!!) ########

@app.get("/actors/id/{actor_id}")
def grt_actor_path(actor_id:int):
    actors = json_to_dict_list(path_to_json)
    for actor in actors:
        if actor.get("id") == actor_id:
            return actor
    raise HTTPException(
        status_code=404,
        detail=f"Актер с таким ID {actor_id} не нфайден"
    )



@app.get("/actors")
def get_all_actors_route(oscar_wins: Optional[int] = None):
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
        "count":len(return_list),
        "actors":return_list
    }

@app.get("/actors/filter/oscar/{oscar_wins}")
def get_all_actors_oscar_wins(
    oscar_wins: int,
    oscar_nominations: Optional[int] = None,
    career_start: Optional[int] = None
    ) -> List[Dict[str, Any]]:
    actors = json_to_dict_list(path_to_json)
    filtered_actors = []
    for actor in actors:
        if actor["oscar_wins"] == oscar_wins:
            filtered_actors.append(actor)
    if oscar_nominations:
            filtered_actors = [actor for actor in filtered_actors if actor["oscar_nominations"] == oscar_nominations]
    if career_start:
            filtered_actors = [actor for actor in filtered_actors if actor['career_start'] == career_start]
    return filtered_actors

@app.get("/actor")
def get_actor_from_param_id(id: int) -> SchemActor:
    actors = json_to_dict_list(path_to_json)
    for actor in actors:
        if actor["id"] == id:
            return actor 


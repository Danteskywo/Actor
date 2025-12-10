from fastapi import FastAPI
from .utils import json_to_dict_list
import os
from typing import Optional
from fastapi.responses import JSONResponse

# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

#Переходим на уровень выше 

parent_dir = os.path.dirname(script_dir)

#Получаем путь к JSON 

path_to_json = os.path.join(parent_dir,'students.json')

app = FastAPI()

@app.get("/actors")
def get_all_students():
    return json_to_dict_list(path_to_json)

@app.get("/")
def home_page():
    message = {"message":"Привет создатель!"}
    return JSONResponse (content=message)

@app.get("/actors/{oscar_wins}")
def get_all_oscar_wins(oscar_wins: int):
    actors = json_to_dict_list(path_to_json)
    return_list = []
    for actor in actors:
        if actor["oscar_wins"] == oscar_wins:
            return_list.append(actor)
    return return_list
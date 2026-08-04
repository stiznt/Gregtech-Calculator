from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dataclasses import dataclass
from fastapi.middleware.cors import CORSMiddleware
from db import Database
from dtypes import *
app = FastAPI()
db = Database()


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/", StaticFiles(directory="frontend/", html=True))

# @app.get("/")
# async def main():
#     return FileResponse("frontend/index.html")

@app.post("/api/add-recipe", status_code=200)
async def add_recipe(recipe:Recipe):
    print("Recipe:", recipe)
    id = db.addRecipe(recipe)
    print("Recipe ID:", id)
    return {"ID": id}

@app.post("/api/add-resource")
async def add_resource(resource: Resource):
    print("Resource:", resource)
    id = db.addResource(resource)
    print("Resource ID:", id)
    return {"ID": id}

@app.post("/api/add-group")
async def add_group(data: Group):
    print("Add group:", data.name)
    id = db.addGroup(data)
    print("Group ID:", id)
    return {"ID": id}

@app.post("/api/add-type")
async def add_type(data:Type):
    print("Add type:", data.name)
    id = db.addType(data)
    print("Type ID:", id)
    return {"ID": id}
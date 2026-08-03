from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dataclasses import dataclass
from fastapi.middleware.cors import CORSMiddleware
from db import Database
from dtypes import Recipe
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

app.mount("/static", StaticFiles(directory="frontend/", html=True))

@app.get("/")
async def main():
    return FileResponse("frontend/index.html")

@app.post("/add-recipe", status_code=200)
async def add_recipe(recipe:Recipe):
    print(recipe)
    db.addRecipe(recipe)
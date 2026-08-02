from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dataclasses import dataclass
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

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

app.mount("/static", StaticFiles(directory="/home/stiznt/gt_python/frontend", html=True))

@app.get("/")
async def main():
    return FileResponse("/home/stiznt/gt_python/frontend/index.html")

class Recipe(BaseModel):
    name: str = Field(alias="recipeName")
    group: str = Field(alias="recipeGroup")
    type: str = Field(alias="recipeType")
    duration: int = Field(alias="recipeDuration")
    tier: int = Field(alias="recipeTier")
    energy: int = Field(alias="recipeEnergy")
    inputs: dict[str, int] = Field(alias="recipeInputs")
    outputs: dict[str, list[int, float]] = Field(alias="recipeOutputs")

@app.post("/add-recipe", status_code=200)
async def add_recipe(recipe:Recipe):
    print(recipe)
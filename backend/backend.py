from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dataclasses import dataclass
from fastapi.middleware.cors import CORSMiddleware
from db import Database
from dtypes import *
from solver import Solver
app = FastAPI()
db = Database()
solver = Solver()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
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

@app.post("/api/solver/add-recipe")
async def solver_add_recipe(data: RecipeID):
    print("Add to solver recipe with ID:", data)
    solver.addRecipe(data)
    return 200

@app.post("/api/solver/set-fixed-recipe")
async def solver_set_fixed(data: RecipeFixed):
    print(f"Set {data.value} value to Recipe with ID:{data.id}")
    solver.setFixed(data.id, data.value)

@app.post("/api/add-recipe-inputs")
async def add_recipe_inputs(data: RecipeInputs):
    print("Add inputs for recipe: ", data.recipeID)
    db.addRecipeInputs(data.recipeID, data.inputs)

@app.post("/api/add-recipe-outputs")
async def add_recipe_outputs(data: RecipeOutputs):
    print("Add outputs for recipe: ", data.recipeID)
    db.addRecipeOutputs(data.recipeID, data.outputs)

@app.get("/api/solver/solve")
async def solver_solve():
    solver.solve()

@app.post("/api/add-recipe-v2")
async def add_recipe_v2(data: RecipeV2):
    print("Add recipe v2")

    recipeTypeID = db.addType(Type(typeName=data.type_name))


    recipeID = db.addRecipe(Recipe(
        recipeName=data.name,
        recipeGroupID=recipeTypeID,
        recipeTypeID=recipeTypeID,
        recipeDuration=data.duration,
        recipeTier=data.tier,
        recipeEnergy=data.energy
    ))

    db.addRecipeInputs(recipeID, data.inputs)
    db.addRecipeOutputs(recipeID, data.outputs)

    print("recipe v2 added")

    
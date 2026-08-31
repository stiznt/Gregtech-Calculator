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
    allow_origin_regex="http://localhost*",
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

# @app.post("/api/add-type")
# async def add_type(data:Type):
#     print("Add type:", data.name)
#     id = db.addType(data)
#     print("Type ID:", id)
#     return {"ID": id}

@app.post("/api/solver/add-recipe")
async def solver_add_recipe(data: RecipeID):
    print("Add to solver recipe with ID:", data)
    solver.addRecipe(data)
    db.addRecipeToSolver(str(data.id))
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

@app.get("/api/get-recipes")
async def get_recipes():
    recipes = db.getRecipes()
    data = [{"id": recipe[0], "name": recipe[1]} for recipe in recipes]
    return data

@app.get("/api/solver/get-recipes")
async def solver_get_recipes() -> list[SolverRecipe]:
    recipes = db.getSolverRecipes()
    result = []

    for recipe in recipes:

        inputs = db.getRecipeInputs(recipe[1])
        inputs = list([SolverRecipeIngredient(resourceName=ingr.name, resourceQuantity=ingr.quantity) for ingr in inputs])
        print(inputs)
        outputs = db.getRecipeOutputs(recipe[1])
        outputs = list([SolverRecipeIngredient(resourceName=ingr.name, resourceQuantity=ingr.quantity) for ingr in outputs])

        result.append(SolverRecipe(
            recipeID=recipe[1],
            recipeName=recipe[4],
            recipeEnergy=recipe[9],
            recipeMult=recipe[2],
            recipeInputs=inputs,
            recipeOutputs=outputs
        ))

    # print(db.getSolverRecipes())
    return result

@app.delete("/api/solver/remove-recipe")
async def solver_remove_recipe(data: RecipeID):
    return db.removeSolverRecipe(str(data.id))

@app.delete("/api/delete-recipe")
async def delete_recipe(data: RecipeID):
    return db.deleteRecipe(str(data.id))
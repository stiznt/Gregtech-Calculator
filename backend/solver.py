from dtypes import *
import pulp
from db import Database

class Solver():

    def __init__(self):
        self.recipes : dict[str, Recipe]= {} 
        self.db = Database()
        self.recipesInputs : dict[str, RecipeInputs] = {}
        self.recipesOutputs: dict[str, RecipeOutputs] = {}
        self.fixed = {}
        self.X = {}


    def addRecipe(self, recipe : RecipeID) -> None:
        self.recipes[recipe.id] = self.db.getRecipe(recipe.id)
        self.recipesInputs[recipe.id] = self.db.getRecipeInputs(recipe.id)
        self.recipesOutputs[recipe.id] = self.db.getRecipeOutputs(recipe.id)

        # Количество машин, для создания одного рецепта в тик
        self.X = {r:pulp.LpVariable(f"X_{r}", lowBound=0) for r in self.recipes}


    def setFixed(self, recipeID:str, machineCount:int) -> None:
        self.fixed[recipeID] =  machineCount


    def solve(self):

        all_resources = set()
        for item in self.recipesInputs:
            all_resources.add(item)
        for item in self.recipesOutputs:
            all_resources.add(item)
                
        prob = pulp.LpProblem("Solver", pulp.LpMinimize)


        #Функция, которую нам надо минимизировать. Функцией является общее количество машин
        prob += pulp.lpSum(self.X[recipe]*self.recipes[recipe].duration for recipe in self.recipes)

        #Балансы по ресурсам: производство должно быть >= потреблению
        for resource in all_resources:
            expr = pulp.lpSum(
                self.X[recipeID] * ((self.recipesOutputs.get(recipeID).getResourceQuantity(resource) - self.recipesInputs[recipeID].getResourceQuantity(resource))/self.recipes[recipeID].duration)
                for recipeID in self.recipes
            )

            #Проверяем есть ли рецепт, который нам генерирует необходимый ресурс
            temp = sum(self.recipesOutputs[recipeID].getResourceQuantity(resource) for recipeID in self.recipes)
            if(temp == 0):
                continue

            prob += expr >= 0

        #Подстановка фиксированных кол-во машин
        for recipeID in self.fixed:
            prob += self.X[recipeID] == self.fixed[recipeID]


        prob.solve()

        if pulp.LpStatus[prob.status] != "Optimal":
            print("Решение не найдено", pulp.LpStatus[prob.status])
        else:
            print("Кол-во станков:")
            for recipeID in self.recipes:
                print(f"{self.recipes[recipeID].name}: {self.X[recipeID].varValue}")

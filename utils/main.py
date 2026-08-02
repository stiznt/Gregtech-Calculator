import pulp
import yaml

recipes = []

#load required recipes
files = ["diesel", "combusion_generate"]

for name in files:
    recipe = yaml.safe_load(open(f"./recipes/{name}.yaml", "r"))
    recipes.append(recipe)

#get all resources from inputs and outputs
products = set()
for recipe in recipes:
    products.update(recipe["inputs"].keys())
    products.update(recipe["outputs"].keys())

products = list(products)
prod_to_index = {p:i for i, p in enumerate(products)}

solver = pulp.LpProblem("Solver", pulp.LpMinimize)

#Variables for LP Solver
X = [pulp.LpVariable(f"x_{r["name"]}", lowBound=0) for r in recipes]

#Функция, которую мы будем минимизировать.
solver += pulp.lpSum(X[i] * recipe["time"] for i, recipe in enumerate(recipes))

#Ограничения по ресурсам
for p in products:
    expr = pulp.lpSum(
        X[i] * ((recipe["outputs"].get(p, 0) - recipe["inputs"].get(p, 0))/recipe["time"])
        for i, recipe in enumerate(recipes)
    )

    #Если у нас нет рецепта на ресурс, то его не надо ограничивать
    count = sum(recipe["outputs"].get(p, 0) for recipe in recipes)
    if count == 0:
        continue

    solver += expr >= 0

#Установка точного количества машинок для производства
idx_gen = next(j for j, r in enumerate(recipes) if r["name"] == "Combution Energy Generate")
max_boule_rate = 21

solver += X[idx_gen] == max_boule_rate, "Exactly_1_Boule_Machine"

solver.solve()

if pulp.LpStatus[solver.status] != "Optimal":
    print("Решение не найдено:", pulp.LpStatus[solver.status])
else:
    print("\nКоличество станков для каждого рецепта:")
    for j, r in enumerate(recipes):
        print(f"{r['name']:45s}: {X[j].varValue:.6f} станков")
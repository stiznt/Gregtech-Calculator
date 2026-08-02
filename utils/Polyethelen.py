import pulp

recipes = [
    {
        "name": "Liquid Polyethylene",
        "time": 160,
        "inputs":{
            "Ethylene": 144,
            "Oxygen Gas": 1000
        },
        "outputs":{
            "Liquid Polyethylene": 216
        }
    },
    {
        "name": "Ethylene",
        "time": 1200,
        "inputs":{
            "Ethanol": 1000,
            "Sulfuric Acid": 1000
        },
        "outputs":{
            "Ethylene": 1000,
            "Diluted Sulfuric Acid": 1000
        }
    },
    {
        "name": "Ethanol",
        "time": 64,
        "inputs":{
            "Biomass": 1000
        },
        "outputs":{
            "Ethanol": 600,
            "Wood pulp": 1
        }
    },
    {
        "name": "Biomass",
        "time": 450,
        "inputs":{
            "Bio Chaff": 4,
            "Water": 4000
        },
        "outputs":{
            "Biomass": 5000
        }
    },
    {
        "name": "Bio Chaff",
        "time": 100,
        "inputs":{
            "Plant Ball": 2
        },
        "outputs":{
            "Bio Chaff": 2
        }
    },
    {
        "name": "Plant Ball",
        "time": 150,
        "inputs":{
            "Potato": 8
        },
        "outputs":{
            "Plant Ball": 1
        }
    },
    {
        "name": "Potato",
        "time": 1200,
        "inputs":{
            "Water": 1000,
            "Fertilizer": 4
        },
        "outputs":{
            "Potato": 48
        }
    },
    {
        "name": "Fertilizer",
        "time": 50,
        "inputs": {
            "Sand": 4,
            "Dirt": 1,
            "Wood Pulp": 2,
            "Water": 1000
        },
        "outputs":{
            "Fertilizer": 4
        }
    },
    {
        "name": "Sulfuric Acid",
        "time": 160,
        "inputs": {
            "Water": 1000,
            "Sulfur Trioxide": 1000
        },
        "outputs": {
            "Sulfuric Acid": 1000
        }
    },
    {
        "name": "Sulfur Trioxide",
        "time": 200,
        "inputs":{
            "Oxygen Gas": 1000,
            "Sulfur Dioxide": 1000
        },
        "outputs": {
            "Sulfur Trioxide": 1000
        }
    },
    {
        "name": "Sulfur Dioxide",
        "time": 60,
        "inputs":{
            "Oxygen Gas": 2000,
            "Sulfur Dust": 1
        },
        "outputs":{
            "Sulfur Dioxide": 1000
        }
    }
]

# Соберём все продукты (входы и выходы)
products = set()
for r in recipes:
    products.update(r["inputs"].keys())
    products.update(r["outputs"].keys())
products = list(products)
prod_to_idx = {p: i for i, p in enumerate(products)}

prob = pulp.LpProblem("Polyethelen", pulp.LpMinimize)

# Переменные: скорость рецептов в циклах в секунду
x = [pulp.LpVariable(f"x_{r['name']}", lowBound=0) for r in recipes]

# idx_diesel = next(j for j, r in enumerate(recipes) if r['name'] == "Diesel")

prob += pulp.lpSum(x[j]*recipes[j]["time"] for j in range(len(recipes)))

# ---------------------------------------------------------
# Баланс по всем продуктам: производство >= потребление
# ---------------------------------------------------------
for p in products:
    expr = pulp.lpSum(
        x[j] * ((r["outputs"].get(p, 0) - r["inputs"].get(p, 0))/r["time"])
        for j, r in enumerate(recipes)
    )

    temp = sum(r["outputs"].get(p, 0) for r in recipes)
    if temp == 0:
        continue
    # Для внешних ресурсов (которые только потребляются и не производятся в этом списке)
    # можно либо не ставить баланс, либо оставить >= 0 — тогда система не сможет их «создать».
    # Здесь оставим >= 0 для всех: если продукт не производится, то его нельзя тратить.
    prob += expr >= 0

idx_gen = next(j for j, r in enumerate(recipes) if r["name"] == "Liquid Polyethylene")
# 1 станок = 1 / boule_time циклов в секунду
max_boule_rate = 1

prob += x[idx_gen] == max_boule_rate, "Exactly_1_Boule_Machine"

prob.solve()

if pulp.LpStatus[prob.status] != "Optimal":
    print("Решение не найдено:", pulp.LpStatus[prob.status])
else:
    print("Статус:", pulp.LpStatus[prob.status])

    print("\nСкорости рецептов (циклов/сек):")
    for j, r in enumerate(recipes):
        print(f"{r['name']:45s}: {x[j].varValue:.6f} циклов/сек")

    print("\nКоличество станков (до округления):")
    for j, r in enumerate(recipes):
        machines = x[j].varValue
        print(f"{r['name']:45s}: {machines:.4f} станков")
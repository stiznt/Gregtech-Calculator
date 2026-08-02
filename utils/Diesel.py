# https://npyscreen.readthedocs.io/introduction.html -> TUI library
import pulp
import yaml

recipes = [
    {
        "name": "Diesel",
        "time": 16,
        "inputs": {
            "Heavy Fuel": 1000,
            "Light Fuel": 5000
        },
        "outputs":{
            "Diesel": 6000
        }
    },
    {
        "name": "Heavy Fuel",
        "time": 160,
        "inputs": {
            "Sulfuric Heavy Fuel": 8000
        },
        "outputs": {
            "Heavy Fuel": 8000
        }
    },
    {
        "name": "Sulfuric Heavy Fuel",
        "time": 20,
        "inputs": {
            "Heavy Oil": 50
        },
        "outputs": {
            "Sulfuric Heavy Fuel": 125
        }
    },
    {
        "name": "Heavy Oil",
        "time": 200,
        "inputs":{
            "Oil Sand": 1
        },
        "outputs":{
            "Heavy Oil": 2000
        }
    },
    {
        "name": "Light Fuel",
        "time": 160,
        "inputs":{
            "Sulfuric Light Fuel": 12000
        },
        "outputs": {
            "Light Fuel": 12000
        }
    },
    {
        "name": "Sulfuric Light Fuel",
        "time": 40,
        "inputs":{
            "Heavy Oil": 100
        },
        "outputs":{
            "Sulfuric Light Fuel": 45
        }
    },
    {
        "name": "EU",
        "time": 15,
        "inputs": {
            "Diesel": 4
        },
        "outputs":{
            "EU": 1920
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

prob = pulp.LpProblem("MaxDiesels", pulp.LpMinimize)

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

idx_gen = next(j for j, r in enumerate(recipes) if r["name"] == "EU")
boule_time = recipes[idx_gen]["time"]
# 1 станок = 1 / boule_time циклов в секунду
diesel_gen_mv = 30 + 1
diesel_gen_hv = 1

prob += x[idx_gen] == diesel_gen_mv + diesel_gen_hv*4, "Exactly_1_Boule_Machine"

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
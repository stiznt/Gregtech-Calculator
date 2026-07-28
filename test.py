import pulp

recipes = [
    {"name": "Basic Integrated Circuit", "time": 200, "inputs": 
     {"Resin Printed Circuit Board": -1, 
      "IC Chip": -1, "Resistor": -2, 
      "Diode": -2, 
      "Fine Copper Wire": -2, 
      "Tin Bolt": -2, 
      "Liquid Soldering Alloy": -72}, 
     "outputs": {"Basic Integrated Circuit": 2}},
    {"name": "IC Chip", "time": 900, "inputs": {"ILC Wafer": -1, "Lubricant": -45}, "outputs": {"IC Chip": 8}},
    {"name": "ILC Wafer", "time": 900, "inputs": {"Silicon Wafer": -1}, "outputs": {"ILC Wafer": 1}},
    {"name": "Silicon Wafer", "time": 400, "inputs": {"Monocrystalline Silicon Boule": -1, "Lubricant": -20}, "outputs": {"Silicon Wafer": 16}},
    {"name": "Monocrystalline Silicon Boule", "time": 9000, "inputs": {"Silicon Dust": -32, "Small Pile of Gallium Arsenide Dust": -1}, "outputs": {"Monocrystalline Silicon Boule": 1}}
]

# Соберём все продукты (входы и выходы)
products = set()
for r in recipes:
    products.update(r["inputs"].keys())
    products.update(r["outputs"].keys())
products = list(products)
prod_to_idx = {p: i for i, p in enumerate(products)}

prob = pulp.LpProblem("Max_Basic_IC_with_1_Boule_Machine", pulp.LpMaximize)

# Переменные: скорость рецептов в циклах в секунду
x = [pulp.LpVariable(f"x_{r['name']}", lowBound=0) for r in recipes]

# ---------------------------------------------------------
# Целевая функция: максимизировать выпуск Basic Integrated Circuit
# ---------------------------------------------------------
idx_basic_ic = next(i for i, r in enumerate(recipes) if r["name"] == "Basic Integrated Circuit")
# За  1 цикл получаем 2 штуки, значит выпуск = x[idx] * 2
prob += x[idx_basic_ic] * recipes[idx_basic_ic]["outputs"]["Basic Integrated Circuit"], "Max_Basic_IC"

# ---------------------------------------------------------
# Баланс по всем продуктам: производство >= потребление
# ---------------------------------------------------------
for p in products:
    expr = pulp.lpSum(
        x[j] * (r["inputs"].get(p, 0) + r["outputs"].get(p, 0))
        for j, r in enumerate(recipes)
    )

    temp = sum(r["outputs"].get(p, 0) for r in recipes)
    if temp == 0:
        continue
    # Для внешних ресурсов (которые только потребляются и не производятся в этом списке)
    # можно либо не ставить баланс, либо оставить >= 0 — тогда система не сможет их «создать».
    # Здесь оставим >= 0 для всех: если продукт не производится, то его нельзя тратить.
    prob += expr >= 0, f"balance_{p}"

# ---------------------------------------------------------
# Ограничение: ровно 1 станок на Monocrystalline Silicon Boule
# ---------------------------------------------------------
idx_boule = next(j for j, r in enumerate(recipes) if r["name"] == "Monocrystalline Silicon Boule")
boule_time = recipes[idx_boule]["time"]
# 1 станок = 1 / boule_time циклов в секунду
max_boule_rate = 1.0 / boule_time

prob += x[idx_boule] == max_boule_rate, "Exactly_1_Boule_Machine"

prob.solve()

if pulp.LpStatus[prob.status] != "Optimal":
    print("Решение не найдено:", pulp.LpStatus[prob.status])
else:
    print("Статус:", pulp.LpStatus[prob.status])
    basic_ic_rate_per_sec = x[idx_basic_ic].varValue * recipes[idx_basic_ic]["outputs"]["Basic Integrated Circuit"]
    basic_ic_per_min = basic_ic_rate_per_sec * 60
    print(f"Максимум Basic Integrated Circuit: {basic_ic_per_min:.2f} в минуту")

    print("\nСкорости рецептов (циклов/сек):")
    for j, r in enumerate(recipes):
        print(f"{r['name']:45s}: {x[j].varValue:.6f} циклов/сек")

    print("\nКоличество станков (до округления):")
    for j, r in enumerate(recipes):
        machines = x[j].varValue * r["time"]
        print(f"{r['name']:45s}: {machines:.4f} станков")

    print("\nКоличество станков (округлённых вверх):")
    for j, r in enumerate(recipes):
        machines_ceil = int(pulp.math.ceil(x[j].varValue * r["time"]))
        print(f"{r['name']:45s}: {machines_ceil} станков")
import numpy as np
from scipy.optimize import linprog

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

all_products = []

for recipe in recipes:
    all_products += list(recipe["inputs"])
    all_products += list(recipe["outputs"])

all_products = list(set(all_products))

all_inputs = []
all_outputs = []

for recipe in recipes:
    all_inputs += recipe['inputs'].keys()
    all_outputs += recipe['outputs'].keys()

all_inputs = list(set(all_inputs))
all_outputs = list(set(all_outputs))

temp = []

for inpt in all_inputs:
    if inpt not in all_outputs:
        temp.append(inpt)

#add global resources input
g_inputs = {"name": "global input", "time": 1, "inputs": {}, "outputs":{}}
for t in temp:
    g_inputs["outputs"][t] = 1
recipes.append(g_inputs)


prod_to_idx = {p: i for i, p in enumerate(all_products)}

n_products = len(all_products)
n_recipes = len(recipes)


A = np.zeros((n_products, n_recipes))

for j, r in enumerate(recipes):
    for p, qty in r["inputs"].items():
        i = prod_to_idx[p]
        A[i, j] += qty
    for p, qty in r["outputs"].items():
        i = prod_to_idx[p]
        A[i, j] += qty

b = np.zeros(n_products)
# target_product = "Monocrystalline Silicon Boule"
# target_rate = 1/9000
# b[prod_to_idx[target_product]] = target_rate

# b[prod_to_idx["Basic Integrated Circuit"]] = 10 * 2/200
# b[prod_to_idx["Monocrystalline Silicon Boule"]] = 1 * 1/9000

c = np.array([r["time"] for r in recipes])

idx = next(j for j, r in enumerate(recipes) if r["name"] == "Basic Integrated Circuit")

c[idx] = -1

A_ub = -A
b_ub = -b

print(A_ub)

A_ub = np.vstack([A_ub, A[prod_to_idx["Monocrystalline Silicon Boule"]]])
b_ub = np.append(b_ub, 1/9000)

# b_ub[prod_to_idx["Monocrystalline Silicon Boule"]] = -b_ub[prod_to_idx["Monocrystalline Silicon Boule"]]

bounds = [(0, None) for _ in range(n_recipes)]

# bounds[prod_to_idx["EU"]] = (1, 1)

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs", options={'disp': True})

if not res.success:
    print(res.message)
else:
    x = res.x
    machines = [x[j] * recipes[j]["time"] for j in range(n_recipes)]  # станки = скорость * время

    for j, recipe in enumerate(recipes):
        print(recipe["name"], x[j]*recipe['time'])
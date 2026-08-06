import sqlite3
from dtypes import *
from uuid6 import UUID
class Database:

    _connection : sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self):
        
        # sqlite3.register_adapter(UUID, lambda u: u.bytes_le)
        # sqlite3.register_converter('UUID', lambda b: UUID(bytes_le=b))

        self._connection = sqlite3.connect("recipes.db", detect_types=sqlite3.PARSE_DECLTYPES)

        self._cursor = self._connection.cursor()

        self.createTables()

    def pushDB(self, sql:str, data:list) -> None:

        if(type(data[0]) in [list, tuple]):
            self._cursor.executemany(sql, data)
        else:
            self._cursor.execute(sql, data)
        self._connection.commit()

    def pullDB(self, sql: str, data:list) -> list:
        self._cursor.execute(sql, data)
        data = self._cursor.fetchall()
        self._connection.commit()
        return data

    def addRecipe(self, recipe: Recipe)->UUID6:

        self.pushDB("INSERT OR IGNORE INTO Recipes (id, name, tier, group_id, type_id, duration, energy) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (str(recipe.id), recipe.name, recipe.tier, str(recipe.group_id), str(recipe.type_id), recipe.duration, recipe.energy))

        return self.pullDB("SELECT id FROM Recipes WHERE name=?", (recipe.name,))[0][0]


    def addResource(self, resource: Resource) -> UUID6:
        self.pushDB("INSERT OR IGNORE INTO Resources (id, name) VALUES (?, ?)", (str(resource.id), resource.name))
        return self.pullDB("SELECT id FROM Resources WHERE name=?", (resource.name,))[0][0]

    def addGroup(self, group: Group) -> UUID6:
        self.pushDB("INSERT OR IGNORE INTO Groups (id, name) VALUES (?, ?)", [str(group.id), group.name])
        return self.pullDB("SELECT id FROM Groups WHERE name=?", (group.name,))[0][0]

    def addType(self, type:Type) -> UUID6:
        self.pushDB("INSERT OR IGNORE INTO Types (id, name) VALUES (?, ?)", [str(type.id), type.name])
        return self.pullDB("SELECT id FROM Types WHERE name=?", (type.name,))[0][0]

    def getRecipe(self, recipeID: str) -> Recipe:
        result = self.pullDB("SELECT * FROM Recipes WHERE id=?", (str(recipeID),))
        if len(result) == 0:
            return None
        return Recipe(
            recipeID=result[0][0],
            recipeName=result[0][1],
            recipeTier=result[0][2],
            recipeGroupID=result[0][3],
            recipeTypeID=result[0][4],
            recipeDuration=result[0][5],
            recipeEnergy=result[0][6]
        )

    def addRecipeInputs(self, recipeID: str, inputs: list[RecipeInputIngredient]):
        for r in inputs:
            resourceID = self.addResource(Resource(resourceID=r.id, resourceName=r.name))

            temp = self.pullDB("SELECT id FROM Inputs WHERE recipe_id=? AND resource_id=?", (str(recipeID), resourceID))
            if len(temp) > 0:
                continue
            self.pushDB("INSERT INTO Inputs (recipe_id, resource_id, quantity) VALUES (?, ?, ?)", (str(recipeID), resourceID, r.quantity))

    def addRecipeOutputs(self, recipeID: str, outputs: list[RecipeOutputIngredient]):
        for r in outputs:
            resourceID = self.addResource(Resource(resourceID=r.id, resourceName=r.name))
            
            temp = self.pullDB("SELECT id FROM Outputs WHERE recipe_id=? AND resource_id=?", (str(recipeID), resourceID))
            if len(temp)>0:
                continue
            self.pushDB("INSERT INTO Outputs (recipe_id, resource_id, quantity, chance) VALUES (?, ?, ?, ?)", (str(recipeID), resourceID, r.quantity, r.chance))

    def getRecipeInputs(self, recipeID: str) -> list[RecipeInputIngredient]:
        result = self.pullDB("SELECT Inputs.resource_id, Inputs.quantity, Resources.name FROM Inputs LEFT JOIN Resources ON Inputs.resource_id=Resources.id WHERE recipe_id=?", (str(recipeID), ))
        res = []
        for item in result:
            res.append(RecipeInputIngredient(resourceID=item[0], quantity=item[1], resourceName=item[2]))
        return res

    def getRecipeOutputs(self, recipeID: str) -> list[RecipeOutputIngredient]:
        result = self.pullDB("SELECT Outputs.resource_id, Outputs.quantity, Outputs.chance, Resources.name FROM Outputs LEFT JOIN Resources ON Outputs.resource_id=Resources.id WHERE recipe_id=?", (str(recipeID), ))
        res = []
        for item in result:
            res.append(RecipeOutputIngredient(resourceID=item[0], resourceName=item[3], quantity=item[1], chance=item[2]))
        return res
        

    def __del__(self):
        self._cursor.close()
        self._connection.close()

    def createTables(self):
        print("create tables")
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Recipes (
            id TEXT PRIMARY KEY UNIQUE,
            name TEXT NOT NULL unique,
            tier int not null,
            group_id UUID not null,
            type_id UUID not null,
            duration integer not null,
            energy integer not null
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Groups (
                id TEXT primary key UNIQUE,
                name text not null unique
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Types (
                id TEXT primary key UNIQUE,
                name text not null unique
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Resources (
                id TEXT primary key UNIQUE,
                name text not null unique
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inputs (
                id integer primary key autoincrement,
                recipe_id integer not null,
                resource_id integer not null,
                quantity integer not null
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Outputs (
                id integer primary key autoincrement,
                recipe_id integer not null,
                resource_id integer not null,
                quantity integer not null,
                chance real not null
            )
        ''')
        self._connection.commit()
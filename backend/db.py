import sqlite3
from dtypes import Recipe
class Database:

    _connection : sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self):
        self._connection = sqlite3.connect("recipes.db")

        self._cursor = self._connection.cursor()

        self.createTables()

    def pushDB(self, sql:str, data:list) -> None:

        if(type(data[0]) in [list, tuple]):
            self._cursor.executemany(sql, data)

        self._cursor.execute(sql, data)

        self._connection.commit()

    def pullDB(self, sql: str, data:list) -> list:
        self._cursor.execute(sql, data)
        return self._cursor.fetchall()

    def addRecipe(self, recipe: Recipe):

        name = recipe.name

        data = self.pullDB("SELECT * from Recipes WHERE name=?", (name, ))

        if(len(data) > 0):
            return

        group_id = self.getGroupIDByName(recipe.group)
        type_id = self.getTypeIDByName(recipe.type)

        duration = recipe.duration
        energy = recipe.energy

        self._cursor.execute(
            "INSERT INTO Recipes (name, group_id, type_id, duration, energy) VALUES (?, ?, ?, ?, ?)",
            (name, group_id, type_id, duration, energy)
        )

        recipe_id = self._cursor.lastrowid

        resources = set()

        resources.update(recipe.inputs.keys())
        resources.update(recipe.outputs.keys())

        resources = list(resources)

        resource_to_id = self.resourcesToID(resources)

        #add inputs
        self._cursor.executemany(
            "INSERT INTO Inputs (recipe_id, resource_id, quantity) VALUES (?, ?, ?)", 
            [(recipe_id, resource_to_id[res], recipe.inputs[res]) for res in recipe.inputs]
        )

        self._cursor.executemany(
            "INSERT INTO Outputs (recipe_id, resource_id, quantity, chance) VALUES (?, ?, ?, ?)", 
            [(recipe_id, resource_to_id[res], recipe.outputs[res][0], recipe.outputs[res][1]) for res in recipe.outputs]
        )
               
        self._connection.commit()

    def resourcesToID(self, resources:list[str]) -> dict[str, int]:
        res = {}

        self._cursor.executemany("INSERT OR IGNORE INTO Resources(name) VALUES (?)", [(resource, ) for resource in resources])

        placeholders = ', '.join("?" for _ in resources)
        self._cursor.execute(f"SELECT id, name from Resources WHERE name in ({placeholders})", resources)

        self._connection.commit()

        for row in self._cursor.fetchall():
            res[row[1]] = row[0]

        return res
    
    def getGroupIDByName(self, group:str) -> int:

        self._cursor.execute("SELECT id FROM Groups WHERE name=?", (group,))
        rows = self._cursor.fetchall()
        if(len(rows) > 0):
            return rows[0][0]

        self._cursor.execute("INSERT INTO Groups (name) VALUES (?)", (group,))

        self._connection.commit()

        return self._cursor.lastrowid

    def getTypeIDByName(self, type:str) -> int:
        self._cursor.execute("SELECT id FROM Types WHERE name=?", (type,))
        rows = self._cursor.fetchall()
        if(len(rows) > 0):
            return rows[0][0]

        self._cursor.execute("INSERT INTO Types (name) VALUES (?)", (type,))

        self._connection.commit()

        return self._cursor.lastrowid

    def __del__(self):
        self._cursor.close()
        self._connection.close()

    def createTables(self):
        print("create tables")
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Recipes (
            id string PRIMARY KEY,
            name TEXT NOT NULL unique,
            group_id integer,
            type_id integer,
            duration integer not null,
            energy integer not null
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Groups (
                id integer primary key autoincrement,
                name text not null unique
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Types (
                id integer primary key autoincrement,
                name text not null unique
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Resources (
                id integer primary key autoincrement,
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
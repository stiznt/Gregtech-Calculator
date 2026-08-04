import sqlite3
from dtypes import *
from uuid6 import UUID
class Database:

    _connection : sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self):
        
        sqlite3.register_adapter(UUID, lambda u: u.bytes_le)
        sqlite3.register_converter('UUID', lambda b: UUID(bytes_le=b))

        self._connection = sqlite3.connect("recipes.db", detect_types=sqlite3.PARSE_DECLTYPES)

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

    def addRecipe(self, recipe: Recipe)->UUID6:

        self.pushDB("INSERT OR IGNORE INTO Recipes (id, name, tier, group_id, type_id, duration, energy) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (recipe.id, recipe.name, recipe.tier, recipe.group_id, recipe.type_id, recipe.duration, recipe.energy))

        return self.pullDB("SELECT id FROM Recipes WHERE name=?", (recipe.name))[0]


    def addResource(self, resource: Resource) -> UUID6:
        self.pushDB("INSERT OR IGNORE INTO Resources (id, name) VALUES (?, ?)", (resource.id, resource.name))
        return self.pullDB("SELECT id FROM Resources WHERE name=?", (resource.name))[0]

    def addGroup(self, name:str) -> UUID6:
        self.pushDB("INSERT OR IGNORE INTO Groups (id, name) VALUES (?, ?)", [uuid6(), name])
        return self.pullDB("SELECT id FROM Groups WHERE name=?", (name,))[0]

    def addType(self, name:str) -> UUID6:
        self.pushDB("INSERT OR IGNORE INTO Types (id, name) VALUES (?, ?)", [uuid6(), name])
        return self.pullDB("SELECT id FROM Types WHERE name=?", (name,))[0]

    
    def __del__(self):
        self._cursor.close()
        self._connection.close()

    def createTables(self):
        print("create tables")
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Recipes (
            id UUID PRIMARY KEY,
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
                id UUID primary key,
                name text not null unique
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Types (
                id UUID primary key,
                name text not null unique
            )
        ''')

        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Resources (
                id UUID primary key,
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
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
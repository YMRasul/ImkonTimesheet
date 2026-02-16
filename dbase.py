import aiosqlite   #pip install aiosqlite
import asyncio
from confvar import DBASE

async def dbase_start():
    print(f"{DBASE=}")
    data = [
        (1, "BOSH OFIS", 40.765167, 72.354389, 25),
        (2, "FURQAT FILIALI", 40.744056, 72.341556, 25),
        (3, "JALAQUDUQ FILIALI", 40.723333, 72.637472, 25),
        (4, "PAXTAOBOD FILIALI", 40.930833, 72.494806, 25),
        (5, "BULOQBOSHI FILIALI", 40.629250, 72.500250, 25),
        (6, "ASAKA FILIALI", 40.645889, 72.244944, 25),
        (7, "JAXON BOZORI FILIALI", 40.824250, 72.351556, 25),
        (8, "FARG'ONA FILIALI", 40.386139, 71.802056, 25),
        (9, "QO'RG'ONTEPA FILIALI", 40.730300, 72.760200, 25),
        (10, "BALIQCHI FILIALI", 40.925500, 71.914400, 25)
        ]
    async with Database(DBASE) as db:
        s = "PRAGMA foreign_keys = ON"
        await db.conn.execute(s)

        s = 'CREATE TABLE IF NOT EXISTS offices ('\
            'id INTEGER PRIMARY KEY,'\
            'name TEXT,lat REAL,lon REAL,'\
            'radius INTEGER DEFAULT 100)'
        await db.conn.execute(s)

        # 2. Вставляем данные в offices
        await db.conn.executemany('''
                         INSERT
                         OR IGNORE INTO offices (id, name, lat, lon, radius) 
            VALUES (?, ?, ?, ?, ?)
                         ''', data)

        s = 'CREATE TABLE IF NOT EXISTS users ( user_id INTEGER PRIMARY KEY, full_name TEXT,  phone TEXT,'
        s = s + 'name TEXT,dolj TEXT,office_id INTEGER,prz INTEGER, dat TEXT, '         # -- формат 'YYYY-MM-DD'
        s = s + 'FOREIGN KEY(office_id) REFERENCES offices(id))'
        await db.conn.execute(s)

        s = 'CREATE TABLE IF NOT EXISTS davomad (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,office_id INTEGER,'
        s = s + ' data TEXT,  time TEXT, prz INTEGER,raz TEXT,FOREIGN  KEY(user_id) REFERENCES  users(user_id) ON DELETE CASCADE)'

        await db.conn.execute(s)

        await db.conn.commit()
    #-----------------------------------------------

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_file)
        self.conn.row_factory = aiosqlite.Row  # Позволяет получать результаты в виде словарей
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.conn.close()

#    async def get_user(self, user_id):
#        return self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    async def fetch_one(self, query: str, params: tuple = ()):
        """Выполняет запрос и возвращает одну строку."""
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, params)
            await self.conn.commit()         # потом добавлен
            return await cursor.fetchone()

    async def fetch_all(self, query: str, params: tuple = ()):
        """Выполняет запрос и возвращает все строки."""
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()

    async def IUD(self, query: str, params: tuple = ()):  # Insert,Update,Delete
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, params)
            await self.conn.commit() # Важно для сохранения!


'''
class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Офисы: id, название, широта, долгота, радиус допустимости (метров)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS offices (
            id INTEGER PRIMARY KEY,
            name TEXT,
            lat REAL,
            lon REAL,
            radius INTEGER DEFAULT 100
        )""")
        # Сотрудники: id, telegram_id, имя, телефон, id_офиса
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            phone TEXT,
            office_id INTEGER,
            dolj TEXT,
            FOREIGN KEY(office_id) REFERENCES offices(id)
        )""")
        self.conn.commit()

    def get_user(self, user_id):
        return self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    def get_office(self, office_id):
        return self.cursor.execute("SELECT * FROM offices WHERE id = ?", (office_id,)).fetchone()

'''
'''

'''
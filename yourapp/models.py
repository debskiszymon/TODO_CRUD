import json
import sqlite3
from sqlite3 import Error

class TodosSQLite:

    def __init__(self):
        self.db_file = "database.db"
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("""
            -- projects table
            CREATE TABLE IF NOT EXISTS tasks (
                id integer PRIMARY KEY,
                name text NOT NULL,
                description text NOT NULL,
                done text not null
            );
            """)

            conn.commit()
    
    def get_all(self):

        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM tasks")
            rows = cur.fetchall()
            return rows

    def get(self, id):

        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM tasks WHERE id=?", (id,))
            rows = cur.fetchone()
            return rows

    def create(self, data):
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            data.pop('csrf_token')
            if data["done"] == 1:
                data["done"] = "tak"
            else:
                data["done"] = "nie"
            values = tuple(v for v in data.values())
            sql = '''INSERT INTO tasks(name, description, done)
                    VALUES(?,?,?)'''
            cur.execute(sql, values)
            conn.commit()
            return cur.lastrowid 

    def update(self, id, data):

        with sqlite3.connect(self.db_file) as conn:

            cur = conn.cursor()
            data.pop('csrf_token')
            if data["done"] == 1:
                data["done"] = "tak"
            else:
                data["done"] = "nie"
            parameters = [f"{k} = ?" for k in data]
            parameters = ", ".join(parameters)
            values = tuple(v for v in data.values())
            values += (id, )

            sql = f''' UPDATE tasks
                        SET {parameters}
                        WHERE id = ?'''
            try:
                cur.execute(sql, values)
                conn.commit()
                print("OK")
            except sqlite3.OperationalError as e:
                print(e)

todossqlite = TodosSQLite()

class Todos:
    def __init__(self):
        try:
            with open("todos.json", "r") as f:
                self.todos = json.load(f)
        except FileNotFoundError:
            self.todos = []

    def all(self):
        return self.todos

    def get(self, id):
        return self.todos[id]

    def create(self, data):
        data.pop('csrf_token')
        self.todos.append(data)

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump(self.todos, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.todos[id] = data
        self.save_all()

todos = Todos()

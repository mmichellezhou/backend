import os
import json
import sqlite3


# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        self.conn = sqlite3.connect("todo.db", check_same_thread=False)
        self.create_task_table()

    def create_task_table(self):
        try:
            self.conn.execute(  # column parameters: name datatype constraints
                """
                CREATE TABLE task (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    DESCRIPTION TEXT NOT NULL,
                    DONE BOOLEAN NOT NULL
                );
            """  # triple quotes allows for multi-line strings
            )  # self.conn.execute() allows for executing a SQL command as provided by a python string
        except Exception as e:
            print(e)

    def get_all_tasks(self):
        # returns an SQLite.Cursor object but can be treated as a 2D array
        cursor = self.conn.execute(
            "SELECT * FROM task;"
        )  # * selects data from all columns in a table
        tasks = []

        # loop over each row and map to its appropriate field name
        for row in cursor:
            tasks.append({"id": row[0], "description": row[1], "done": row[2]})

        return tasks

    def insert_task_table(self, description, done):
        cursor = self.conn.cursor()  # instantiates a cursor; self.conn.execute is a shortcut that instatiates a cursor, executes the SQL command, and returns the cursor

        cursor.execute(
            "INSERT INTO task (DESCRIPTION, DONE) VALUES (?, ?);", (description, done)
        )  # ? mark placeholder values; actual values are provided inside a tuple as a second argument
        self.conn.commit()  # saves any changes to the database
        return cursor.lastrowid

    def get_task_by_id(self, id):
        cursor = self.conn.execute("SELECT * FROM task WHERE ID = ?", (id,))

        # returns one row of data if our task exists, or not at all otherwise
        for row in cursor:
            return {"id": row[0], "description": row[1], "done": row[2]}

        return None

    def update_task_by_id(self, id, description, done):
        self.conn.execute(
            """
            UPDATE task
            SET description = ?, done = ?
            WHERE id = ?;
        """,
            (description, done, id),
        )
        self.conn.commit()

    def delete_task_by_id(self, id):
        self.conn.execute(
            """
            DELETE FROM task
            WHERE id = ?;
        """,
            (id,),
        )
        self.conn.commit()


# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)

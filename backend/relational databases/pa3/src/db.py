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
        """
        Secures a connection with the database and stores it into the
        instance variable `conn`
        """
        self.conn = sqlite3.connect("todo.db", check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.create_user_table()
        self.create_transaction_table()


    def create_user_table(self):
        """
        Using SQL, creates a user table
        """
        try:
            self.conn.execute(
                """
                CREATE TABLE user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    balance INTEGER
                );
            """
            )
        except Exception as e:
            print(e)

    def get_all_users(self):
        """
        Using SQL, gets all users from the user table
        """
        cursor = self.conn.execute("SELECT id, name, username FROM user;")
        tasks = []

        for row in cursor:
            tasks.append({"id": row[0], "name": row[1], "username": row[2]})

        return tasks

    def insert_user_table(self, name, username, balance):
        """
        Using SQL, adds a new user in the user table
        """
        cursor = self.conn.cursor()

        cursor.execute(
            "INSERT INTO user (name, username, balance) VALUES (?, ?, ?);",
            (name, username, balance),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_user_by_id(self, id):
        """
        Using SQL, gets a user by id
        """
        cursor = self.conn.execute("SELECT * FROM user WHERE id = ?", (id,))

        for row in cursor:
            return {
                "id": row[0],
                "name": row[1],
                "username": row[2],
                "balance": row[3],
                "transactions": self.get_transactions_by_user_id(id),
            }

        return None

    def delete_user_by_id(self, id):
        """
        Using SQL, deletes a user by id
        """
        self.conn.execute(
            """
            DELETE FROM user
            WHERE id = ?;
        """,
            (id,),
        )
        self.conn.commit()
        

    def send_money_by_id(self, sender_id, receiver_id, amount):
        """
        Using SQL, sends money from one user to another by id
        """
        cursor = self.conn.execute("SELECT * FROM user WHERE id = ?", (sender_id,))

        for row in cursor:
            new_balance = row[3] - amount
            self.conn.execute(
                """
                UPDATE user
                SET balance = ?
                WHERE id = ?;
            """,
                (new_balance, sender_id),
            )
            self.conn.commit()

        cursor = self.conn.execute("SELECT * FROM user WHERE id = ?", (receiver_id,))

        for row in cursor:
            new_balance = row[3] + amount
            self.conn.execute(
                """
                UPDATE user
                SET balance = ?
                WHERE id = ?;
            """,
                (new_balance, receiver_id),
            )
            self.conn.commit()

    def create_transaction_table(self):
        """
        Using SQL, creates a transaction table
        """
        try:
            self.conn.execute(
                """
                CREATE TABLE transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    accepted BOOLEAN,
                    FOREIGN KEY(sender_id) REFERENCES user(id) ON DELETE CASCADE,
                    FOREIGN KEY(receiver_id) REFERENCES user(id) ON DELETE CASCADE
                );
            """
            )
        except Exception as e:
            print(e)

    def get_transactions_by_user_id(self, id):
        """
        Using SQL, gets a transaction by user id
        """
        cursor = self.conn.execute(
            "SELECT * FROM transactions WHERE sender_id = ? OR receiver_id = ?",
            (id, id),
        )
        transactions = []

        for row in cursor:
            transactions.append(
                {
                    "id": row[0],
                    "timestamp": row[1],
                    "sender_id": row[2],
                    "receiver_id": row[3],
                    "amount": row[4],
                    "message": row[5],
                    "accepted": row[6],
                }
            )

        return transactions

    def insert_transaction_table(
        self, timestamp, sender_id, receiver_id, amount, message, accepted
    ):
        """
        Using SQL, adds a new transaction in the transaction table
        """
        cursor = self.conn.cursor()

        cursor.execute(
            "INSERT INTO transactions (timestamp, sender_id, receiver_id, amount, message, accepted) VALUES (?, ?, ?, ?, ?, ?);",
            (timestamp, sender_id, receiver_id, amount, message, accepted),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_transaction_by_id(self, id):
        """
        Using SQL, gets a transaction by id
        """
        cursor = self.conn.execute("SELECT * FROM transactions WHERE id = ?", (id,))

        for row in cursor:
            return {
                "id": row[0],
                "timestamp": row[1],
                "sender_id": row[2],
                "receiver_id": row[3],
                "amount": row[4],
                "message": row[5],
                "accepted": row[6],
            }

        return None

    def accept_or_deny_request(self, id, timestamp, accepted):
        """
        Using SQL, accepts or denies a request transaction by id
        """
        self.conn.execute(
            """
            UPDATE transactions
            SET timestamp = ?, accepted = ?
            WHERE id = ?;
        """,
            (timestamp, accepted, id),
        )
        self.conn.commit()


# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)

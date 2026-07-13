import sqlite3


class DatabaseManager:

    def __init__(self, db_path="parking.db"):

        self.db_path = db_path

        self.create_table()

    def connect(self):

        return sqlite3.connect(self.db_path)

    def create_table(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_records (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            plate_number TEXT,

            entry_time TEXT,

            exit_time TEXT,

            status TEXT,

            parking_fee REAL

        )
        """)

        conn.commit()

        conn.close()
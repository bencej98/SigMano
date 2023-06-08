import sqlite3
import os.path
from datetime import datetime

class Gnome_Database:
    path = f"game_database_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.db"

    def __init__(self) -> None:
        pass

    def create_table(self):
        '''Creates the database'''
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS "user" (
                "ID" INTEGER NOT NULL,
                "username" TEXT UNIQUE,
                "password" TEXT,
                "gnome" TEXT UNIQUE,
                "sumscore" INTEGER,
                PRIMARY KEY("ID" AUTOINCREMENT)
            )''')
        self.conn.commit()
        print("")

    def create_time_stamp(self):
        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M")
        return current_time
        



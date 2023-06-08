import sqlite3
import os.path
from datetime import datetime

class Gnome_Database:
    # path = f"game_database_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.db"
    path = "game_database.db"

    def __init__(self) -> None:
        self.connect = sqlite3.connect(self.path)
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        '''Creates the database'''
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS "user" (
                "id" INTEGER NOT NULL,
                "username" TEXT UNIQUE,
                "password" TEXT,
                "gnome" TEXT UNIQUE,
                "sumscore" INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
            )''')
        
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS "match" (
            "match_id"	INTEGER NOT NULL,
            "user_id"	INTEGER NOT NULL,
            "kill_count"	INTEGER,
            "score"	INTEGER,
            "date" DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY("match_id" AUTOINCREMENT)
            )'''
        )
        self.connect.commit()
        # self.connect.close()
        print("")
        
    def close_connection(self):
        '''Closes the database connection'''
        self.cursor.close()
        self.connect.close()

    def create_user(self, username, password):
        '''Inserts user into database'''
        self.cursor.execute('''
                        INSERT INTO user
                        VALUES(?, ?)
                        '''
                         , (username, password))
        self.connect.commit()
    
    def delete_user(self, username):
        self.cursor.execute("DELETE FROM user WHERE username = ?", (username,))
        row_count = self.cursor.rowcount

        if row_count > 0:
            print("Delete successful. Rows affected:", row_count)
        else:
            print("No rows deleted. The username may not exist or match any records.")

        self.connect.commit()

    def print_sum_point(self, username):
        self.cursor.execute('''
                        SELECT sumscore FROM user
                        WHERE username = ?
                        '''
                         , (username,))
        print(f"TEST user's score: {self.cursor.fetchone()[0]}")

jatek = Gnome_Database()
jatek.create_table()
jatek.close_connection()

# '''
# SELECT score
# FROM match
# INNER JOIN user
# ON user.id = match.user_id
# '''

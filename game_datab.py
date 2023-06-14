import sqlite3
import logging
from datetime import datetime
import json


class Gnome_Database:
    path = "game_database.db"

    def __init__(self) -> None:
        self.connect = sqlite3.connect(self.path)
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        """Creates the database"""
        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS "user" (
                    "id" INTEGER NOT NULL,
                    "username" TEXT UNIQUE,
                    "password" TEXT,
                    "gnome" TEXT UNIQUE,
                    "sumscore" INTEGER,
                    PRIMARY KEY("id" AUTOINCREMENT)
                )"""
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS "match" (
                "match_id"	INTEGER NOT NULL,
                "username"	TEXT,
                "kill_count"	INTEGER,
                "score"	INTEGER,
                "date" TEXT NOT NULL,
                PRIMARY KEY("match_id" AUTOINCREMENT)
                )"""
            )
            self.connect.commit()
            logging.info("Database tables created successfully.")
        except sqlite3.Error as e:
            error_msg = "Error creating database tables: %s" % str(e)
            logging.error(error_msg)
            print(error_msg)

    def close_connection(self):
        """Closes the database connection"""
        try:
            self.cursor.close()
            self.connect.close()
            logging.info("Database connection closed.")
        except sqlite3.Error as e:
            error_msg = "Error closing database connection: %s" % str(e)
            logging.error(error_msg)
            print(error_msg)

    def create_user(self, username: str, password: str, gnome_name) -> bool | None:
        """Inserts user into database"""
        try:
            self.cursor.execute(
                """
                            INSERT INTO user
                            VALUES(?, ?, ?, ?, ?)
                            """,
                (None, username, password, gnome_name, None),
            )
            self.connect.commit()
            logging.info("New user created: %s", username)
            return True
        except sqlite3.Error as e:
            error_msg = "Error creating user: %s" % str(e)
            logging.error(error_msg)
            print(error_msg)

    def delete_user(self, username: str) -> None:
        """Deletes user from the database"""
        try:
            self.cursor.execute("DELETE FROM user WHERE username = ?", (username,))
            row_count = self.cursor.rowcount

            if row_count > 0:
                logging.info("User deleted: %s. Rows affected: %s", username, row_count)
            else:
                logging.warning("No rows deleted. The username may not exist or match any records.")

            self.connect.commit()
        except sqlite3.Error as e:
            error_msg = "Error deleting user: %s" % str(e)
            logging.error(error_msg)
            print(error_msg)

    def print_sum_point(self, username: str) -> None:
        """Prints out the sum of the points of the user"""
        try:
            self.cursor.execute(
                """
                            SELECT sumscore FROM user
                            WHERE username = ?
                            """,
                (username,),
            )
            sumscore = self.cursor.fetchone()[0]
            logging.info("User's score: %s", sumscore)
            print(f"TEST user's score: {sumscore}")
        except sqlite3.Error as e:
            error_msg = "Error retrieving user's score: %s" % str(e)
            logging.error(error_msg)
            print(error_msg)

    def add_results_upon_death(self, username: str, kill_count: int, score: int) -> None:
        """Adds results upon death to the database"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute(
                """
                            INSERT INTO match
                            VALUES (?, ?, ?, ?, ?)
            """,
                (None, username, kill_count, score, current_time),
            )

            self.connect.commit()
            logging.info("Results added upon death for user: %s. Kill count: %s, Score: %s", username, kill_count, score)
            self.update_sumscore_upon_death(username, score)
        except sqlite3.Error as e:
            error_msg = "Error adding results upon death: %s" % str(e)
            logging.error(error_msg)
            print(error_msg)

    def update_sumscore_upon_death(self, username: str, score: int) -> None:
        """"Updates the sum of the point uf the user upon death"""
        try:
            self.cursor.execute(
                """
                        UPDATE user
                        SET sumscore = sumscore + ?
                        WHERE username = ?
                        """,
                (score, username),
            )

            self.connect.commit()
            logging.info("Sum score updated for user: %s", username)
        except sqlite3.Error as e:
            error_msg = "Error updating sum score: %s" % str(e)
            logging.error(error_msg)
            print(error_msg)

    def send_auth_json(self, authentication_bool: bool) -> json:
        """Sends back the result of the authentication or registartion to the client"""
        authentication_data = {
                                "Type": "Auth", "Payload": authentication_bool
                            }
        return json.dumps(authentication_data)

    def check_user_upon_registration(self, username: str, password: str):
        """Checks if a user already exists in the database in case of registration"""
        user_lower = username.lower()
        self.cursor.execute("""
                        SELECT *
                        FROM user
                        WHERE username = ?
                        """
                        , (user_lower,))
        validator = self.cursor.fetchone()
        if validator is None:
            gnome_name = f"gnome_{user_lower}"
            self.create_user(user_lower, password, gnome_name)
            return self.send_auth_json(True)
        else:
            return self.send_auth_json(False)

    def login_user(self, username: str, password: str):
        """Validates the user in case of login"""
        user_lower = username.lower()
        self.cursor.execute("""
            SELECT username, password
            FROM user
            WHERE username = ?
            """
            , (user_lower,))
        user_data = self.cursor.fetchone()
        if user_data is None:
            return self.send_auth_json(False)
        else:
            if user_data[1] == password:
                return self.send_auth_json(True)
            else:
                return self.send_auth_json(False)


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    filename='server.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    jatek = Gnome_Database()
except sqlite3.Error as e:
    error_msg = "Error initializing Gnome_Database: %s" % str(e)
    logging.error(error_msg)
    print(error_msg)


jatek = Gnome_Database()

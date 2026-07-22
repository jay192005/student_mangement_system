import mysql.connector

class Database:
    def __init__(self):

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jay@2005",
            database="school_db"
        )

        self.cursor = self.connection.cursor(dictionary=True)

    def execute(self, query, values=None):

        self.cursor.execute(query, values)
        self.connection.commit()

    def fetch_one(self, query, values=None):

        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def fetch_all(self, query, values=None):

        self.cursor.execute(query, values)
        return self.cursor.fetchall()

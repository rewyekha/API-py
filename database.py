import mysql.connector

class Database:
    def __init__(self):
        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='chs'
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, data=None):
        # Execute SQL query
        if data:
            self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)

    def fetch_one(self):
        # Fetch one record
        return self.cursor.fetchone()

    def fetch_all(self):
        # Fetch all records
        return self.cursor.fetchall()

    def commit(self):
        # Commit transaction
        self.conn.commit()

    def rollback(self):
        # Rollback transaction
        self.conn.rollback()

    def close_connection(self):
        # Close database connection
        self.cursor.close()
        self.conn.close()

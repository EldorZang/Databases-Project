import mysql.connector

class DatabaseConnectionError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Database Connection Error: {self.message}"

class DatabaseQueryError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Database Query Error: {self.message}"

class UserExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"User Exists Error: {self.message}"

class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Authentication Error: {self.message}"

class DatabaseError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Database Error: {self.message}"

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="FunGeo"
        )
        return connection
    except mysql.connector.errors.ProgrammingError as err:
        raise DatabaseConnectionError("Please check your database connection settings.") from err
    except mysql.connector.Error as err:
        raise DatabaseConnectionError("Please check your database connection settings.") from err

def execute_query(query, params=None):
    try:
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        raise DatabaseQueryError("An error occurred while fetching data from the database.") from err
    finally:
        if 'connection' in locals():
            connection.close()

def execute_update(query, params=None):
    try:
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        raise DatabaseQueryError("An error occurred while updating data in the database.") from err
    finally:
        if 'connection' in locals():
            connection.close()

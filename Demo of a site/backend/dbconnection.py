import mysql.connector
from mysql.connector import IntegrityError

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

class IntegrityDataError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"IntegrityDataError: {self.message}"

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


class GeneralError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Error: {self.message}"

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
    except Exception as err:
        raise GeneralError(str(err))
def execute_query(query, params=None):
    try:
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)
        
        # Print the query with parameters
        if params:
            formatted_query = query.format(**params)
        else:
            formatted_query = query
        print("Executing query:", formatted_query)
        
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        raise DatabaseQueryError("An error occurred while fetching data from the database.") from err
    except Exception as err:
        raise GeneralError(str(err))
    finally:
        if 'connection' in locals():
            connection.close()


def execute_update(query, params=None):
    try:
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)
        if params:
            formatted_query = query.format(**params)
        else:
            formatted_query = query
        print("Executing update:", formatted_query)
        cursor.execute(query, params)
        connection.commit()
    except IntegrityError as err:
        raise IntegrityDataError("Integrity error, a possible violation of schema definition.") from err
    except mysql.connector.Error as err:
        raise DatabaseQueryError("An error occurred while updating data in the database.") from err
    except Exception as err:
        raise GeneralError(str(err))
    finally:
        if 'connection' in locals():
            connection.close()

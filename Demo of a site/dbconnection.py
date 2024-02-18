import mysql.connector
import sys

def connect_db():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="FunGeo"
        )
        return connection
    except mysql.connector.errors.ProgrammingError as err:
        print("Error connecting to the database:", err)
        print("Access denied. Please check your database username and password.")
        sys.exit(1)
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        print("Please check your database connection settings.")
        sys.exit(1)

def execute_query(query, params=None):
    connection = connect_db()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print("Error executing query:", err)
        print("An error occurred while fetching data from the database.")
        # sys.exit(1)
    finally:
        if connection:
            connection.close()

def execute_update(query, params=None):
    connection = connect_db()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        print("Error updating data:", err)
        print("An error occurred while updating data in the database.")
        # sys.exit(1)
    finally:
        if connection:
            connection.close()

import mysql.connector
import sys
from mysql.connector import IntegrityError

def connect_db():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="FunGeo"
        )
        return connection
    except mysql.connector.errors.ProgrammingError as err:
        raise Exception("Error connecting to the database.<br>Access denied. Please check your database username and password.<br>" + str(err))
    except mysql.connector.Error as err:
        raise Exception("Error connecting to the database.<br>Please check your database connection settings.<br>" + str(err))

def execute_query(query, params=None):
    connection = connect_db()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        raise Exception("Error executing query.<br>An error occurred while fetching data from the database.<br>" + str(err))
    finally:
        if connection:
            connection.close()

def execute_update(query, params=None):
    connection = connect_db()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        connection.commit()
    except IntegrityError as err:
        raise err
    except mysql.connector.Error as err:
        raise Exception("Error updating data.<br>An error occurred while updating data in the database.<br>" + str(err))
    finally:
        if connection:
            connection.close()

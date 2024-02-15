import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="FunGeo"
    )
    return connection

def execute_query(query, params=None):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query, params)
    result = cursor.fetchall()

    connection.close()
    return result

def execute_update(query,params=None):
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query,params)
        connection.commit()
        connection.close()
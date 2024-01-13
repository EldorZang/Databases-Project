import mysql.connector

# Connect to the MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Create the FunGeo database
cursor.execute("CREATE DATABASE IF NOT EXISTS FunGeo")
connection.commit()

# Switch to the FunGeo database
cursor.execute("USE FunGeo")

# Create the 'user' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    )
""")

# Create the 'subject' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subject (
        subject_id INT AUTO_INCREMENT PRIMARY KEY,
        subject_name VARCHAR(255) NOT NULL
    )
""")

# Create the 'exam' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Exam (
        user_id INT NOT NULL,
        subject_id INT NOT NULL,
        grade INT,
        PRIMARY KEY (user_id, subject_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
    )
""")

# Create the 'continent' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Continent (
        continent_name VARCHAR(255) PRIMARY KEY
    )
""")

# Create the 'country' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Country (
        country_code VARCHAR(255) PRIMARY KEY,
        currency VARCHAR(255) NOT NULL,
        flag_image_url VARCHAR(255),
        country_name VARCHAR(255) NOT NULL,
        region VARCHAR(255),
        population INT,
        continent_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (continent_name) REFERENCES Continent(continent_name)
    )
""")

# Create the 'city' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS City (
        city_id INT AUTO_INCREMENT PRIMARY KEY,
        city_name VARCHAR(255) NOT NULL,
        country_code VARCHAR(255) NOT NULL,
        FOREIGN KEY (country_code) REFERENCES Country(country_code)
    )
""")

# Create the 'capital' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Capital (
        country_code VARCHAR(255) PRIMARY KEY,
        city_id INT NOT NULL,
        FOREIGN KEY (country_code) REFERENCES Country(country_code),
        FOREIGN KEY (city_id) REFERENCES City(city_id)
    )
""")

# Commit the changes and close the connection
connection.commit()
connection.close()

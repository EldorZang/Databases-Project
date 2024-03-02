import mysql.connector
import pandas as pd
import random
import string
import zipfile

# Connect to the MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="fungeo"
)

# Create a cursor object to interact with the database
cursor = connection.cursor(buffered=True)

# Function to insert data into a table
def insert_data(table_name, mapping_columns, values):
    columns = ', '.join(mapping_columns)
    placeholders = ', '.join(['%s'] * len(mapping_columns))

    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
    connection.commit()

# Function to insert data into the Country table
def insert_country_data():
    countries_df = pd.read_csv("countries_continents_codes_flags_url.csv")
    world_data_df = pd.read_csv("world_data_2023.csv")
    countries_of_the_world_df = pd.read_csv("countries_of_the_world.csv")
    continents_df = pd.read_csv("countries.csv")

    for _, row in countries_df.iterrows():
        country_code = str(row['alpha-2']).strip()

        if country_code not in ['BQ', 'KR', 'PS', 'SH', 'nan'] and not pd.isnull(country_code):
            flag_image_url_bck = "https://vectorflags.s3-us-west-2.amazonaws.com/flags/"+str.lower(country_code)+"-flag-01.png"
            flag_image_url = str(row['image_url']).strip() if not pd.isnull(row['image_url']) else flag_image_url_bck
            country_name = str(row['country']).strip() if not pd.isnull(row['country']) else 'UNKNOWN'

            region_population_data = countries_of_the_world_df.loc[countries_of_the_world_df['Country'].str.strip() == country_name]
            region = str(region_population_data['Region'].values[0]).strip() if not region_population_data.empty else 'UNKNOWN'
            population = int(region_population_data['Population'].values[0]) if not region_population_data.empty else random.randint(10000, 10000000)

            currency_data = world_data_df.loc[world_data_df['Country'] == country_name]
            random_uppercase_letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))

            if not currency_data.empty and not pd.isnull(currency_data['Currency-Code'].values[0]):
                currency = str(currency_data['Currency-Code'].values[0]).strip()
            else:
                currency = random_uppercase_letters

            continent_data = continents_df.loc[continents_df['Country'] == country_name]
            continent_values = ["North America", "Asia", "Europe", "South America", "Oceania", "Africa"]
            continent_name = str(continent_data['Continent'].values[0]).strip() if not continent_data.empty else random.choice(continent_values)

            insert_data("Country", ["country_code", "flag_image_url", "country_name", "region", "population", "currency", "continent_name"],
                        (country_code, flag_image_url, country_name, region, population, currency, continent_name))

# Function to check if the country code exists in the Country table
def country_code_exists(country_code):
    # Execute a SQL query to check for the existence of the country code
    query = "SELECT * FROM Country WHERE country_code = %s"
    # Execute the query and check if any rows are returned
    result = cursor.execute(query, (country_code,))
    return cursor.fetchone() is not None

# Function to insert data into the City table
def insert_city_data():
    with zipfile.ZipFile("worldcitiespop.zip", "r") as zip_ref:
        # Assuming there's only one file in the zip archive
        csv_filename = zip_ref.namelist()[0]
        with zip_ref.open(csv_filename) as csv_file:
            cities_pop_df = pd.read_csv(csv_file, low_memory=False)

            # Capitalize values in the "Country" column
            cities_pop_df['Country'] = cities_pop_df['Country'].str.upper()

            for _, row in cities_pop_df.iterrows():
                country_code = str(row['Country']).strip().upper()  # Convert country code to uppercase

                # Check if the country code exists in the Country table before inserting
                if country_code_exists(country_code):
                    city_name = str(row['AccentCity']).strip() if not pd.isnull(row['AccentCity']) else 'UNKNOWN'
                    insert_data("City", ["city_name", "country_code"], (city_name, country_code))

# Function to insert data into the Capital table
def insert_capital_data():
    world_data_df = pd.read_csv("world_data_2023.csv")

    for _, row in world_data_df.iterrows():
        country_abbreviation = str(row['Abbreviation']).strip()
        city_name = str(row['Capital/Major City']).strip()

        if country_abbreviation not in ['BQ', 'KR', 'PS', 'SH'] and not pd.isnull(country_abbreviation):
            cursor.execute("SELECT country_code FROM Country WHERE country_code = %s", (country_abbreviation,))
            country_result = cursor.fetchone()

            if country_result:
                cursor.execute("SELECT city_id FROM City WHERE city_name = %s", (city_name,))
                city_result = cursor.fetchone()

                if city_result:
                    city_id = city_result[0]
                else:
                    cursor.execute("INSERT INTO City (city_name, country_code) VALUES (%s, %s)", (city_name, country_abbreviation))
                    connection.commit()

                    cursor.execute("SELECT city_id FROM City WHERE city_name = %s", (city_name,))
                    city_result = cursor.fetchone()
                    city_id = city_result[0]

                country_code = country_abbreviation

                insert_data("Capital", ["country_code", "city_id"], (country_code, city_id))

# Function to insert data into the Continent table
def insert_continent_data():
    continent_values = ["North America", "Asia", "Europe", "South America", "Oceania", "Africa"]
    for value in continent_values:
        insert_data("Continent", ["continent_name"], (value,))

# Uncomment the function calls based on your needs
insert_continent_data()
insert_country_data()
insert_city_data()
insert_capital_data()

# Close the connection
connection.close()

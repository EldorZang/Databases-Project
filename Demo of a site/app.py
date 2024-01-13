from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="fungeo"
    )
    return connection

def get_flags():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT Country.country_name, Country.flag_image_url
        FROM Country
    """

    cursor.execute(query)
    flags_data = cursor.fetchall()

    connection.close()
    return flags_data

def get_capital_cities():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT Country.country_name, City.city_name
        FROM Country
        JOIN Capital ON Country.country_code = Capital.country_code
        JOIN City ON Capital.city_id = City.city_id
    """

    cursor.execute(query)
    capital_cities_data = cursor.fetchall()

    connection.close()
    return capital_cities_data

def get_currencies():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT Country.country_name, Country.currency
        FROM Country
    """

    cursor.execute(query)
    currencies_data = cursor.fetchall()

    connection.close()
    return currencies_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_topic', methods=['POST'])
def select_topic():
    selected_topic = request.form['topic']
    data = None

    if selected_topic == 'flags':
        data = get_flags()
    elif selected_topic == 'capital_cities':
        data = get_capital_cities()
    elif selected_topic == 'currencies':
        data = get_currencies()

    if data is not None:
        return render_template('result.html', topic=selected_topic, data=data)
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)

# app.py
from flask import Flask, redirect, render_template, request, session, url_for
import mysql.connector
import dbconnection

app = Flask(__name__)
app.secret_key = 'secret_key'


def get_flags(continent=None, population=None, order_by='country_name'):
    query = """
        SELECT Country.country_name, Country.flag_image_url
        FROM Country
    """
    
    conditions = []
    params = {}

    if continent:
        conditions.append("Country.continent_name = %(continent)s")
        params['continent'] = continent

    if population:
        population_value = int(population.replace('Up to ', '').replace(',', ''))
        conditions.append("Country.population <= %(population)s")
        params['population'] = population_value

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += f" ORDER BY {order_by}"
    return execute_query(query, params)

def get_capital_cities(continent=None, order_by='city_name'):
    query = """
        SELECT Country.country_name, City.city_name
        FROM Country
        JOIN Capital ON Country.country_code = Capital.country_code
        JOIN City ON Capital.city_id = City.city_id
    """

    if continent:
        query += " WHERE Country.continent_name = %(continent)s"
    
    query += f" ORDER BY {order_by}"
    return execute_query(query, {'continent': continent})

def get_currencies(order_by='currency'):
    query = """
        SELECT Country.country_name, Country.currency
        FROM Country
    """

    query += f" ORDER BY {order_by}"
    return execute_query(query)

def get_currencies_by_continent(continent, order_by='currency'):
    query = """
        SELECT Country.country_name, Country.currency
        FROM Country
        WHERE Country.continent_name = %(continent)s
    """

    query += f" ORDER BY {order_by}"
    return execute_query(query, {'continent': continent})

def get_currencies_by_population(population, order_by='currency'):
    query = """
        SELECT Country.country_name, Country.currency
        FROM Country
        WHERE Country.population <= %s
    """

    population_value = int(population.replace('Up to ', '').replace(',', ''))

    query += f" ORDER BY {order_by}"
    return execute_query(query, (population_value,))

@app.route('/')
def index():
    return redirect(url_for('login')) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'bob' and password == '1234':
            # Successful login, redirect to main menu
            session['username'] = username
            return redirect(url_for('main_menu'))
        else:
            # Incorrect username or password, set error message
            error = 'Incorrect username or password. Please try again.'
    
    # Render the login page with error message (if any)
    return render_template('login.html', error=error)

@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

@app.route('/select_topic', methods=['POST'])
def select_topic():
    selected_topic = request.form['topic']
    data = None

    if selected_topic == 'flags':
        continent = request.form.get('filterOption') if request.form.get('complexity') == 'continent' else None
        population = request.form.get('filterOption') if request.form.get('complexity') == 'population' else None
        order_by = request.form.get('order_by', 'country_name')

        data = get_flags(continent=continent, population=population, order_by=order_by)

    elif selected_topic == 'capital_cities':
        continent = request.form.get('filterOption') if request.form.get('complexity') == 'continent' else None
        order_by = request.form.get('order_by', 'city_name')

        data = get_capital_cities(continent=continent, order_by=order_by)

    elif selected_topic == 'currencies':
        # Handle the case when the user chooses the category of "continent"
        if request.form.get('advanced_study') == 'on' and request.form.get('complexity') == 'continent':
            continent = request.form.get('filterOption')
            data = get_currencies_by_continent(continent)
        elif request.form.get('advanced_study') == 'on' and request.form.get('complexity') == 'population':
            population = request.form.get('filterOption')
            data = get_currencies_by_population(population)
        else:
            # Handle other cases (if needed)
            order_by = request.form.get('order_by', 'currency')
            data = get_currencies(order_by=order_by)

    if data is not None:
        return render_template('result.html', topic=selected_topic, data=data)
    else:
        return render_template('error.html')


@app.route('/user_personal_area')
def personal_area():
    if 'username' in session:
        current_username = session['username']  # Retrieve current username from session
        return render_template('user_personal_area.html', current_username=current_username)
    else:
        return redirect(url_for('login'))  # Redirect to login page if user not logged in

@app.route('/logout')
def logout():
    # Clear username from session
    session.pop('username', None)
    return redirect(url_for('login'))  # Redirect to login page after logout

if __name__ == '__main__':
    app.run(debug=True)

# app.py
import json
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import mysql.connector
import dbconnection
from learn_queries import get_countries_data
import user_queries
app = Flask(__name__)
app.secret_key = 'secret_key123'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

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
        
        if user_queries.authenticate_login(username,password):
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


@app.route('/user_personal_area', methods=['GET', 'POST'])
def personal_area():
    if 'username' in session:
        current_username = session['username']  # Retrieve current username from session
        if request.method == 'GET':
            return render_template('user_personal_area.html', current_username=current_username)
        if request.method == 'POST':
            newPassword = request.form['newPassword']
            user_queries.update_password(current_username,newPassword)
            return redirect(url_for('main_menu'))


    else:
        return redirect(url_for('login'))  # Redirect to login page if user not logged in

@app.route('/logout')
def logout():
    # Clear username from session
    session.pop('username', None)
    return redirect(url_for('login'))  # Redirect to login page after logout

@app.route('/delete_user')
def delete_user():
    if 'username' in session:
        current_username = session['username']
        user_queries.delete_user(current_username)
        session.pop('username', None)
    return redirect(url_for('login'))  # Redirect to login page after logout

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_queries.register(username,password)
        return redirect(url_for('login'))  # Redirect to login page after registration

    users_count = user_queries.count_uesrs()
    return render_template('register.html',users_count=users_count)


@app.route('/learn_results')
def learn_results():
    data = app.data
    columns = json.loads(request.args.get('options'))
    return render_template('learn_results.html', countries=data,options=columns)



@app.route('/learn', methods=['GET', 'POST'])
def learn():
    if request.method == 'POST':
        country_input = request.form['searchInput']
        columns = request.form.getlist('option')
        data = get_countries_data(country_input,columns)
        selected_options = [{'name': col.capitalize()} for col in columns]
        app.data = data
        return redirect(url_for('learn_results',options=json.dumps(selected_options)))

    return render_template('learn.html')


if __name__ == '__main__':
    app.run(debug=True)

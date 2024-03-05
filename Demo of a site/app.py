import json
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from learn_queries import get_countries_data , get_complex_data,get_countries_lst,get_cities
import user_queries,test_queries
from dbconnection import DatabaseConnectionError, DatabaseQueryError
from user_queries import count_users
from site_queries import total_subjects , unexplored_subjects , repeat_users , all_subjects ,top_scores_for_subject

app = Flask(__name__)
app.secret_key = 'secret_key123'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

tests_length = 10


def user_logged():
    if 'username' in session:
        return True
    return False

# Define custom error pages
@app.errorhandler(DatabaseConnectionError)
@app.errorhandler(DatabaseQueryError)
@app.errorhandler(Exception)
def handle_database_error(error):
    return render_template('error.html', error=error), 500

@app.route('/test_menu')
def test_menu():
        if not user_logged(): return redirect(url_for('login'))
        return render_template('test_menu.html')

@app.route('/test')
def test():
        if not user_logged(): return redirect(url_for('login'))
        subject = request.args.get('subject')
        
        if not subject: return redirect(url_for('test_menu'))
        test,test_correct = test_queries.get_test(tests_length,subject)
        app.test = test
        app.test_correct = test_correct
        app.subject = subject

        return render_template('test.html', questions=test,subject=subject)

@app.route('/submit_test', methods=['POST'])
def submit_test():
    # Get user's answers from the form
    user_answers = {}
    questions = app.test
    correct_answers = app.test_correct
    for question in questions.keys():
        user_answers[question] = request.form.get(question, '')

    # Calculate correct count
    correct_count = 0
    for question, answer in user_answers.items():
        if answer == correct_answers.get(question):
            correct_count += 1

    app.correct_count = correct_count
    app.test_score = int(round((correct_count/len(questions))*100,0))
    app.user_answers = user_answers

    test_queries.update_user_test_score(session['username'],app.subject,app.test_score)
    # Render the result page with the user's answers and correct count
    return redirect(url_for('test_result'))
    

@app.route('/test_result')
def test_result():
        if not user_logged(): return redirect(url_for('login'))
        questions = app.test
        correct_answers = app.test_correct
        user_answers = app.user_answers
        correct_count = app.correct_count
        test_score = app.test_score
        subject = app.subject
        return render_template('test_result.html', questions=questions, correct_answers=correct_answers, user_answers=user_answers, correct_count=correct_count,
                            total_questions=len(questions),test_score=test_score,subject=subject)
    
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if user_queries.authenticate_login(username, password):
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
    if not user_logged(): return redirect(url_for('login'))
    return render_template('main_menu.html')

@app.route('/select_topic', methods=['POST'])
def select_topic():
    selected_topic = request.form['topic']
    data = None

    try:
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
    except (DatabaseConnectionError, DatabaseQueryError) as e:
        return render_template('error.html', error=e), 500

    if data is not None:
        return render_template('result.html', topic=selected_topic, data=data)
    else:
        return render_template('error.html', error="Error retrieving data"), 500

@app.route('/user_personal_area', methods=['GET', 'POST'])
def personal_area():
    if not user_logged(): return redirect(url_for('login'))

    current_username = session['username']  # Retrieve current username from session
    if request.method == 'GET':
        # Retrieve additional statistics
        subjects_studied = user_queries.amount_of_subjects_studied(current_username)
        average_score = user_queries.average_score(current_username)
        if average_score is None:
            average_score = 0
        exclusive_subjects = user_queries.subjects_unstudied_by_others(current_username)
        highest_grade_subjects = user_queries.subjects_with_higher_grades(current_username)
        
        return render_template('user_personal_area.html', current_username=current_username,
                                subjects_studied=subjects_studied,
                                average_score=average_score, exclusive_subjects=exclusive_subjects,
                                highest_grade_subjects=highest_grade_subjects)
    if request.method == 'POST':
        newPassword = request.form['newPassword']
        user_queries.update_password(current_username, newPassword)
        return redirect(url_for('main_menu'))



@app.route('/logout')
def logout():
    if not user_logged(): return redirect(url_for('login'))
    # Clear username from session
    session.pop('username', None)
    return redirect(url_for('login'))  # Redirect to login page after logout

@app.route('/delete_user')
def delete_user():
    if not user_logged(): return redirect(url_for('login'))
    current_username = session['username']
    user_queries.delete_user(current_username)
    session.pop('username', None)

    return redirect(url_for('login'))  # Redirect to login page after logout

@app.route('/register', methods=['GET', 'POST'])
def register():
    users_count = user_queries.count_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_queries.register(username, password):
            return redirect(url_for('login'))  # Redirect to login page after registration
        else:
            # User already exists, set error message
            error = 'User already exists. Please choose a different username.'
            # Render the register page with error message (if any)
            return render_template('register.html', users_count=users_count, error=error)
    return render_template('register.html', users_count=users_count)


@app.route('/learn_results')
def learn_results():
    if not user_logged(): return redirect(url_for('login'))
    data = app.data
    columns = json.loads(request.args.get('options'))
    return render_template('learn_results.html', countries=data,options=columns)

@app.route('/learn_results_cities')
def learn_results_cities():
    if not user_logged(): return redirect(url_for('login'))
    cities = app.data
    country_name = request.args.get('country_name')
    return render_template('learn_results_cities.html', cities=cities,country_name=country_name)

@app.route('/learn_countries', methods=['GET', 'POST'])
def learn_countries():
    if not user_logged(): return redirect(url_for('login'))
    if request.method == 'POST':
        country_input = request.form['searchInput']
        columns = request.form.getlist('option')
        data = None
        selected_options = [{'name': col.capitalize()} for col in columns]
        
        if 'advanced_study' in request.form:
            complexity = request.form['complexity']
            filter_option = request.form['filterOption']
            data = get_complex_data(country_input, columns, complexity, filter_option)
            # selected_options.append({'name': complexity.capitalize(), 'value': filter_option})
        else:
            data = get_countries_data(country_input, columns)


        app.data = data
        return redirect(url_for('learn_results', options=json.dumps(selected_options)))

    return render_template('learn_countries.html')


@app.route('/learn_cities', methods=['GET', 'POST'])
def learn_cities():
    if not user_logged(): return redirect(url_for('login'))
    if request.method == 'POST':
        country_input = request.form['country']
        num_results = request.form['num_results']
        order = request.form['order']
        
        data = get_cities(country_input,num_results,order)
        app.data = data
        return redirect(url_for('learn_results_cities', country_name=country_input))
    countries_lst = get_countries_lst()

    return render_template('learn_cities.html',countries=countries_lst)




@app.route('/statistics')
def statistics():
    if not user_logged(): return redirect(url_for('login'))
    # Example: Retrieve statistics data from database
    num_registered_users = count_users()
    num_total_subjects = total_subjects()
    num_unexplored_subjects = unexplored_subjects()
    num_repeat_users = repeat_users()
    subjects = all_subjects()

    return render_template('statistics.html', num_registered_users=num_registered_users,
                           total_subjects=num_total_subjects, unexplored_subjects=num_unexplored_subjects,
                           repeat_users=num_repeat_users, subjects=subjects)



@app.route('/top_scores', methods=['POST'])
def top_scores():
    if not user_logged(): return redirect(url_for('login'))
    data = request.get_json()
    subject = data.get('subject')
    # Assuming you have a function to retrieve top scores based on the selected subject
    top_scores_data = top_scores_for_subject(subject)
    return jsonify(top_scores_data)



if __name__ == '__main__':
    app.run(debug=True)

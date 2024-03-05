from mysql.connector import IntegrityError
import dbconnection
from dbconnection import DatabaseError,GeneralError
from random import randrange

def get_subject_id(subject):
        params = {'subject': subject}
        return (dbconnection.execute_query("SELECT subject_id from Subject where subject_name = %(subject)s", params)[0]['subject_id'])

def get_user_id(username):
        params = {'username': username}
        return (dbconnection.execute_query("SELECT user_id from User where username = %(username)s",params)[0]['user_id'])

def update_user_test_score(username,subject,score):
        user_id = get_user_id(username)
        subject_id=get_subject_id(subject)

        # remove the current score (if exists)
        params = {'user_id': user_id,'subject_id': subject_id}
        dbconnection.execute_update("DELETE FROM Exam WHERE user_id = %(user_id)s AND subject_id = %(subject_id)s", params)
        # Insert new test data

        params = {'user_id': user_id,'subject_id': subject_id, 'score': score}
        dbconnection.execute_update("INSERT INTO Exam (user_id, subject_id, grade) VALUES (%(user_id)s, %(subject_id)s, %(score)s)", params)


def random_insert(lst, element):
    lst.insert(randrange(len(lst)+1), element)

def get_flag_question():
    # Step 1: Select a random country along with its flag and continent
    question_data = (dbconnection.execute_query("""
                                    SELECT
                                    country_name AS correct_option,
                                    flag_image_url AS question,
                                    continent_name
                                    FROM Country
                                    ORDER BY RAND()
                                    LIMIT 1"""))[0]
    
    # Step 2: Select three random countries from the same continent as the question country as options
    params = {'continent_name': question_data['continent_name'], 'country_name': question_data['correct_option']}
    wrong_answers_data = dbconnection.execute_query("""
                                            SELECT country_name
                                            FROM Country
                                            WHERE continent_name = %(continent_name)s AND country_name != %(country_name)s
                                            ORDER BY RAND()
                                            LIMIT 3""",params)
    question = question_data['question']
    correct_answer = question_data['correct_option']
    wrong_answers = [x['country_name'] for x in wrong_answers_data]
    return (question,correct_answer,wrong_answers)

def get_test_data(test_length,get_question_func):
    test = {}
    test_correct = {}
    for i in range(test_length):
        question,correct_answer,wrong_answers = get_question_func()
        answers = wrong_answers
        random_insert(answers,correct_answer)
        test[question] = answers
        test_correct[question] = correct_answer
    return test,test_correct


def get_captial_cities_question():
    # Step 1: Select a random country and its capital city
    question_data = (dbconnection.execute_query("""
                                    SELECT
                                    Country.country_name AS question,
                                    Capital.city_id,
                                    Capital.country_code,
                                    City.city_name AS correct_option
                                    FROM
                                    Country
                                    JOIN
                                    Capital ON Country.country_code = Capital.country_code
                                    JOIN
                                        City ON City.city_id = Capital.city_id
                                    WHERE
                                        City.city_name <>'NaN'
                                    ORDER BY RAND()
                                    LIMIT 1"""))[0]
    
    # Step 2: Select three random countries from the same continent as the question country as options
    params = {'country_code': question_data['country_code'], 'city_id': question_data['city_id']}
    wrong_answers_data = dbconnection.execute_query("""
                                                    SELECT City.city_name,City.city_id,City.country_code
                                                    FROM City
                                                    JOIN
                                                    Country ON City.country_code = Country.country_code
                                                    JOIN
                                                    Capital ON Country.country_code = Capital.country_code
                                                    WHERE
                                                    City.country_code = %(country_code)s 
                                                    AND City.city_id != %(city_id)s 
                                                    AND City.city_name <> 'NaN'
                                                    ORDER BY RAND()
                                                    LIMIT 3""",params)
    question = question_data['question']
    correct_answer = question_data['correct_option']
    wrong_answers = [x['city_name'] for x in wrong_answers_data]
    return (question,correct_answer,wrong_answers)

def get_currency_question():
    # Step 1: Select a random currency and a country where it's used
    question_data = (dbconnection.execute_query("""
                                                SELECT Country.currency AS question,
                                                Country.country_name AS correct_option,
                                                Country.currency,
                                                Country.continent_name,
                                                Country.country_code
                                                FROM Country 
                                                ORDER BY RAND()
                                                LIMIT 1"""))[0]
    
    # Step 2: Select three random countries from the same continent as options, excluding the country where the currency is used
    params = {'country_code': question_data['country_code'], 'currency': question_data['currency'],'continent_name':question_data['continent_name']}
    wrong_answers_data = dbconnection.execute_query("""
                                                    SELECT DISTINCT
                                                    country_name
                                                    FROM Country
                                                    WHERE country_code != %(country_code)s 
                                                    AND currency !=  %(currency)s 
                                                    AND continent_name = %(continent_name)s 
                                                    ORDER BY RAND()
                                                    LIMIT 3""",params)
    question = question_data['question']
    correct_answer = question_data['correct_option']
    wrong_answers = [x['country_name'] for x in wrong_answers_data]
    return (question,correct_answer,wrong_answers)




def get_test(test_length,subject):
      test_funcs = {
            'Flags': get_flag_question,
            'Capitals_Cities': get_captial_cities_question,
            'Currencies': get_currency_question
      }
      return get_test_data(test_length,test_funcs[subject])








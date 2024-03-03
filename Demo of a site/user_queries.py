import dbconnection
from dbconnection import DatabaseError

def user_exists(username):
    try:
        params = {'username': username}
        res = dbconnection.execute_query("SELECT COUNT(*) AS user_count FROM User WHERE username = %(username)s", params)
        return res[0]['user_count'] > 0
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while checking if user exists.") from err

def register(username, password):
    try:
        if user_exists(username):
            return False
        params = {'username': username, 'password_hash': password}
        dbconnection.execute_update("INSERT INTO User (username, password_hash) VALUES (%(username)s, %(password_hash)s)", params)
        return True
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while registering user.") from err

def authenticate_login(username, password):
    try:
        params = {'username': username, 'password_hash': password}
        res = dbconnection.execute_query("SELECT * FROM User WHERE username = %(username)s AND password_hash = %(password_hash)s", params)
        #if not res:
        #    raise AuthenticationError("Invalid username or password.")
        return res
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while authenticating user.") from err

def update_password(username, newpassword):
    try:
        params = {'username': username, 'new_password_hash': newpassword}
        dbconnection.execute_update("UPDATE User SET password_hash = %(new_password_hash)s WHERE username = %(username)s", params)
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while updating password.") from err

def delete_user(username):
    try:
        params = {'username': username}
        dbconnection.execute_update("DELETE FROM User WHERE username = %(username)s", params)
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while deleting user.") from err

def count_users():
    try:
        res = dbconnection.execute_query("SELECT COUNT(*) AS user_count FROM User")
        return res[0]['user_count']
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while counting users.") from err

def amount_of_subjects_studied(username):
    try:
        params = {'username': username}
        res = dbconnection.execute_query("""
            SELECT COUNT(DISTINCT subject_id) AS subject_count 
            FROM Exam e 
            JOIN User u ON e.user_id = u.user_id 
            WHERE u.username = %(username)s
        """, params)
        return res[0]['subject_count']
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while retrieving the amount of subjects studied by the user.") from err

def average_score(username):
    try:
        params = {'username': username}
        res = dbconnection.execute_query("""
            SELECT AVG(grade) AS average_score 
            FROM Exam e 
            JOIN User u ON e.user_id = u.user_id 
            WHERE u.username = %(username)s
        """, params)
        return res[0]['average_score']
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while retrieving the average score of the user.") from err

def subjects_unstudied_by_others(username):
    try:
        params = {'username': username}
        res = dbconnection.execute_query("""
            SELECT COUNT(DISTINCT e.subject_id) AS subject_count 
            FROM Exam e 
            JOIN User u ON e.user_id = u.user_id 
            WHERE e.subject_id NOT IN (
                SELECT DISTINCT subject_id 
                FROM Exam 
                WHERE user_id != (
                    SELECT user_id FROM User WHERE username = %(username)s
                )
            ) AND u.username = %(username)s
        """, params)
        return res[0]['subject_count']
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while retrieving the amount of subjects studied by the user that no other user has studied.") from err

def subjects_with_higher_grades(username):
    try:
        params = {'username': username}
        res = dbconnection.execute_query("""
            SELECT COUNT(DISTINCT e1.subject_id) AS subject_count 
            FROM Exam e1 
            JOIN User u ON e1.user_id = u.user_id 
            WHERE e1.grade > (
                SELECT MAX(grade) 
                FROM Exam 
                WHERE subject_id = e1.subject_id 
                AND user_id != (
                    SELECT user_id FROM User WHERE username = %(username)s
                )
            ) 
            AND u.username = %(username)s
        """, params)
        return res[0]['subject_count']
    except dbconnection.DatabaseQueryError as err:
        raise DatabaseError("An error occurred while retrieving the number of subjects studied by the user that no other user received a higher grade than.") from err

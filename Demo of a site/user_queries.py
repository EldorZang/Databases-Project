import dbconnection
from dbconnection import DatabaseError, UserExistsError,AuthenticationError

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

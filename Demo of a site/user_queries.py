from mysql.connector import IntegrityError
import dbconnection
"""
def user_exists(username):
    params = {'username': username}
    res = dbconnection.execute_query("SELECT COUNT(*) AS user_count FROM User WHERE username = %(username)s", params)
    return res[0]['user_count'] > 0
"""
def register(username,password):
    """
    # Check if the user already exists
    if user_exists(username):
        return False
    """
    try:
        params = {'username':username,'password_hash':password}
        dbconnection.execute_update("INSERT INTO User (username, password_hash) VALUES (%(username)s, %(password_hash)s)",params)
    # Case the user name already exists
    except IntegrityError:
        return "IntegrityError"
    except Exception as e:
        raise Exception(e)
    return "Success"

def authenticate_login(username,password):
    params = {'username':username,'password_hash':password}
    res = dbconnection.execute_query("SELECT * FROM User WHERE username = %(username)s AND password_hash = %(password_hash)s",params)
    return res 
    
def update_password(username,newpassword):
    params = {'username':username,'new_password_hash':newpassword}
    dbconnection.execute_update("UPDATE User SET password_hash = %(new_password_hash)s WHERE username =  %(username)s",params)



def delete_user(username):
    params = {'username': username}
    dbconnection.execute_update("DELETE FROM User WHERE username =  %(username)s",params)

def count_uesrs():
    res = dbconnection.execute_query("SELECT COUNT(*) AS user_count FROM User")
    return res[0]['user_count']


    
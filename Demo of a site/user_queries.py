import dbconnection
def register(username,password):
    params = {}
    params['username'] = username
    params['password_hash'] = password
    dbconnection.execute_update("INSERT INTO User (username, password_hash) VALUES (%(username)s, %(password_hash)s)",params)

def authenticate_login(username,password):
    params = {}
    params['username'] = username
    params['password_hash'] = password
    res = dbconnection.execute_query("SELECT * FROM User WHERE username = %(username)s AND password_hash = %(password_hash)s",params)
    if res:
        return True
    else:
        return False 
    
def update_password(username,newpassword):
    params = {}
    params['username'] = username
    params['new_password_hash'] = newpassword
    dbconnection.execute_update("UPDATE User SET password_hash = %(new_password_hash)s WHERE username =  %(username)s",params)


def delete_user(username):
    params = {}
    params['username'] = username
    dbconnection.execute_update("DELETE FROM User WHERE username =  %(username)s",params)

def count_uesrs():
    res = dbconnection.execute_query("SELECT COUNT(*) AS user_count FROM User")
    return res[0]['user_count']


    
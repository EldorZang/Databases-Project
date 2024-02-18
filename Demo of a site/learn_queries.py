import dbconnection
def get_countries_data(country_name,columns):
    #query = "SELECT " + columns_str + " FROM Country WHERE country_name like '%" + country_name + "%'"
    if 'capital' in columns:
        columns.remove('capital')
        if len(columns) > 0:
            columns_str = ''.join(f'country.{x},' for x in columns)
        else:
            columns_str = ''
        columns.append('capital')
        query = "  SELECT " + columns_str + " city_name as capital " + " FROM Country"
        query += " JOIN capital on capital.country_code = Country.country_code"
        query += " JOIN city ON City.city_id = capital.city_id"
        query += " WHERE country_name like '%" + country_name + "%'"
    else:
        if len(columns) > 0:
            columns_str = ''.join(f'{x},' for x in columns)[:-1]
        else:
            columns_str = ''   
        query = "  SELECT " + columns_str + " FROM Country WHERE country_name like '%" + country_name + "%'"
     
    res = dbconnection.execute_query(query)
    return res

print(get_countries_data('Israel',['capital']))









    
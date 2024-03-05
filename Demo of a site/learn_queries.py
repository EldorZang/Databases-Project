import dbconnection

def get_cities(country_name,num_results,order):
    #params = {'country_name': country_name,'num_results':num_results,'order':order}
    query = f"""
            SELECT city_name,City.population
            FROM City
            JOIN
            Country
            ON City.country_code  = Country.country_code
            WHERE Country.country_name = '{country_name}' 
            ORDER BY City.population {order} 
            LIMIT {num_results}
            """
    res = dbconnection.execute_query(query)
    return res   

def get_countries_lst():
    data =  dbconnection.execute_query("""
                                      SELECT country_name
                                      FROM Country
                                      ORDER BY country_name
                                      """)
    return [x['country_name'] for x in data]

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
        query = "  SELECT " + columns_str + " FROM Country WHERE country_name like '%" + country_name + "%'" + "ORDER BY country_name"
     
    res = dbconnection.execute_query(query)
    return res


def get_complex_data(country_name, columns, complexity, filter_option):
    if complexity == 'continent':
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
            query += f" WHERE country_name like '%{country_name}%' AND continent_name = '{filter_option}'"
        else:
            if len(columns) > 0:
                columns_str = ''.join(f'{x},' for x in columns)[:-1]
            else:
                columns_str = ''   
            query = f"SELECT {columns_str} FROM Country WHERE country_name like '%{country_name}%' AND continent_name = '{filter_option}'"

    elif complexity == 'population':
        # Assuming filter_option is in format 'Up to XXXX' where XXXX is a number
        population_limit = int(filter_option.split()[-1].replace(',', ''))
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
            query += f" WHERE country_name like '%{country_name}%' AND population <= {population_limit}"
        else:
            if len(columns) > 0:
                columns_str = ''.join(f'{x},' for x in columns)[:-1]
            else:
                columns_str = ''   
            query = f"SELECT {columns_str} FROM Country WHERE country_name like '%{country_name}%' AND population <= {population_limit}"
    else:
        # Handle other complexities if needed
        pass
    
    res = dbconnection.execute_query(query)
    return res






    
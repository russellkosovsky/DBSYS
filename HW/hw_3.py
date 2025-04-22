import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='136.244.224.221',
            user='com303rkosovsky',
            password='rk3536rk',
            database='com303rkosovsky'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# to execute SQL queries
def execute_query(connection, query, values=None):
    try:
        cursor = connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        return cursor
    except Error as e:
        print(f"Error: {e}")
        return None


# read data from the file and insert into the tables
def insert_data_from_file(filename):
    try:
        connection = create_connection()
        if connection:
            col_names = None 
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split('\t')
                    table_name = data[0]

                    if table_name == "Table" or table_name == "":
                        col_names = data[1:]
                        pass
                    else:
                        values = tuple(data[1:])

                        # Check if the row already exists in the table
                        placeholders = ' and '.join([f'{col} = "{values[col_names.index(col)]}"' for col in col_names])
                        check_query = f"select count(*) from {table_name} where {placeholders};"


                        print("CHECK QUERY: ", check_query)

                        #cursor = execute_query(connection, check_query, values)
                        cursor = execute_query(connection, check_query)

                        if cursor:
                            count = cursor.fetchone()[0]

                            # If the row doesn't exist, insert it
                            if count == 0:
                                print("count is 0!!!")
                                insert_query = f"insert into {table_name} values ({', '.join(['%s' for _ in values])});"
                                print("INSERT QUERY: ", insert_query)
                                execute_query(connection, insert_query, values)

            # commit the changes
            connection.commit()
            print("Data inserted successfully.")
    except Error as e:
        # rollback if an error occurs
        connection.rollback()
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()



######################################################################################
# QUESTION 3
# Using the tables above, write python code to get the name of each employee and the 
# city that they work in. Turn in the code and the output.
######################################################################################

### QUESTION 3a
def q_3a():
    connection = create_connection()
    query = '''select e.Name, e.City 
            from employee e 
            inner join works w on e.Id = w.Id;
            '''
    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    for result in results:
        print(f"Employee Name: {result[0]}, City: {result[1]}")

### QUESTION 3b
def q_3b():
    connection = create_connection()
    # Query to get employee IDs and their corresponding cities
    query_ids_cities = '''
                        select e.Id, e.City
                        from employee e
                        inner join works w on e.Id = w.Id;
                        '''

    cursor = connection.cursor()
    cursor.execute(query_ids_cities)

    results = cursor.fetchall()

    # Use the results to query for employee names
    for result in results:
        employee_id = result[0]
        city = result[1]

        query_names = f'''
                        select Name
                        from employee
                        where Id = '{employee_id}';
                        '''

        cursor.execute(query_names)
        name_result = cursor.fetchone()

        if name_result:
            employee_name = name_result[0]
            print(f"Employee Name: {employee_name}, City: {city}")



######################################################################################
# QUESTION 4
# Using the tables above, write python code to get the name of each employee and the 
# name of their manager. Turn in the code and the output.
######################################################################################

def q_4a():
    connection = create_connection()
    query = '''
            select e.Name as EN, m.Name as MN
            from employee e
            left join manager m1 on e.Id = m1.e_Id
            left join employee m on m1.m_Id = m.Id;
            '''

    cursor = connection.cursor()
    cursor.execute(query)

    results = cursor.fetchall()

    for result in results:
        employee_name = result[0]
        manager_name = result[1] if result[1] else "No Manager"
        print(f"Employee Name: {employee_name}, Manager Name: {manager_name}")


def q_4b():
    connection = create_connection()

    # Query to get employee IDs and their corresponding manager IDs
    query_ids = '''
                                    select e.Id as EId, m.m_Id as MId
                                    from employee e
                                    left join manager m on e.Id = m.e_Id;
                                    '''
    

    cursor = connection.cursor()
    cursor.execute(query_ids)
    
    results_ids = cursor.fetchall()

    # Use the results to query for employee and manager names
    for result in results_ids:
        employee_id = result[0]
        manager_id = result[1]

        # Query to get employee and manager names
        query_names = f'''
                        select e.Name as EName, m.Name as MName
                        from employee e
                        left join manager mgr on e.Id = mgr.e_Id
                        left join employee m on mgr.m_Id = m.Id
                        where e.Id = '{employee_id}';
                        '''

        cursor.execute(query_names)
        name_result = cursor.fetchone()

        employee_name = name_result[0]
        manager_name = name_result[1] if name_result[1] else "No Manager"
        print(f"Employee Name: {employee_name}, Manager Name: {manager_name}")



def main():

    # please note that In order for it to work, you must change Employee Id to e_Id 
    # and Manager Id to m_Id within the text file. I know that is not really allowed but i ran out of time.
    filename = "homework_3.problem_2.data.txt"
    #insert_data_from_file(filename)
    
    #q_3a()
    #q_3b()
    #q_4a()
    #q_4b()

main()

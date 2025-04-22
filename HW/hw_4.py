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



#######################################################################################
##
## QUESTION 3a
##

def avg_salary(company_name):
    try:
        connection = create_connection()
        if connection:
            query = f"SELECT AVG(salary) FROM works WHERE company = '{company_name}';"
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()[0]
            return result
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

average_salary = avg_salary("First Bank")
print(f"Average Salary at First Bank: {average_salary}")

#######################################################################################


#######################################################################################
##
## QUESTION 3b
##

def higher_average_salary_companies():
    try:
        connection = create_connection()
        if connection:
            query = '''
                SELECT company
                FROM works
                GROUP BY company
                HAVING AVG(salary) > (SELECT AVG(salary) FROM works WHERE company = 'First Bank');
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

higher_salary_companies = higher_average_salary_companies()
print("Companies with Higher Average Salary:")
for company in higher_salary_companies:
    print(company[0])

#######################################################################################




#######################################################################################
##
## QUESTION 4a
##

def get_instructor_class_student():
    try:
        connection = create_connection()
        if connection:
            query = '''
                SELECT
                    instructor.name AS InstructorName,
                    class.name AS ClassName,
                    student.name AS StudentName
                FROM
                    instructor
                    JOIN teaches ON instructor.id = teaches.instructor_id
                    JOIN class ON teaches.class_id = class.id
                    JOIN enrolled ON class.id = enrolled.class_id
                    JOIN student ON enrolled.student_id = student.id
                ORDER BY
                    instructor.name,
                    class.name,
                    student.name;
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

instructor_class_student_data = get_instructor_class_student()
print("Instructor, Class, Student Data:")
for row in instructor_class_student_data:
    print(row)

#######################################################################################




#######################################################################################
##
## QUESTION 4b
##

def get_instructor_class_student():
    try:
        connection = create_connection()
        if connection:
            # Execute queries step by step
            query_instructors = 'SELECT * FROM instructor;'
            cursor = connection.cursor()
            cursor.execute(query_instructors)
            instructors = cursor.fetchall()

            # Process instructors and get their classes and students
            for instructor in instructors:
                instructor_id = instructor[0]
                query_classes = f'SELECT * FROM teaches WHERE instructor_id = {instructor_id};'
                cursor.execute(query_classes)
                classes = cursor.fetchall()

                for class_record in classes:
                    class_id = class_record[1]
                    query_students = f'''
                        SELECT student.name
                        FROM enrolled
                        JOIN student ON enrolled.student_id = student.id
                        WHERE enrolled.class_id = {class_id};
                    '''
                    cursor.execute(query_students)
                    students = cursor.fetchall()

                    # Print the results
                    print(f"Instructor: {instructor[1]}, Class: {class_record[1]}, Students: {', '.join([student[0] for student in students])}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

get_instructor_class_student()

#######################################################################################

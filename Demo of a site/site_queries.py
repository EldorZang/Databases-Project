from dbconnection import execute_query
from dbconnection import DatabaseError

def total_subjects():
    try:
        query = """
            SELECT COUNT(DISTINCT subject_id) AS total_subjects
            FROM Subject
        """
        result = execute_query(query)
        return result[0]['total_subjects']
    except DatabaseError as e:
        # Handle database query error
        raise DatabaseError("An error was occurred.") from e

def unexplored_subjects():
    try:
        query = """
            SELECT COUNT(*) AS unexplored_subjects
            FROM Subject
            WHERE subject_id NOT IN (
                SELECT DISTINCT subject_id FROM Exam
            )
        """
        result = execute_query(query)
        return result[0]['unexplored_subjects']
    except DatabaseError as e:
        # Handle database query error
        raise DatabaseError("An error was occurred.") from e

def repeat_users():
    try:
        query = """
            SELECT COUNT(user_id) AS repeat_users
            FROM (
                SELECT user_id FROM Exam
                GROUP BY user_id
                HAVING COUNT(subject_id) > 1
            ) AS repeat_users
        """
        result = execute_query(query)
        return result[0]['repeat_users']
    except DatabaseError as e:
        # Handle database query error
        raise DatabaseError("An error was occurred.") from e

def all_subjects():
    try:
        query = """
            SELECT subject_name
            FROM Subject
        """
        result = execute_query(query)
        subject_names = [row['subject_name'] for row in result]
        return subject_names
    except DatabaseError as e:
        # Handle database query error
        raise DatabaseError("An error was occurred.") from e

def top_scores_for_subject(subject):
    try:
        params = {'subject': subject}
        res = execute_query("""
            SELECT u.username, e.grade
            FROM Exam e
            JOIN User u ON e.user_id = u.user_id
            JOIN Subject s ON e.subject_id = s.subject_id
            WHERE s.subject_name = %(subject)s
            ORDER BY e.grade DESC
            LIMIT 3
        """, params)
        top_scores = [{'username': row['username'], 'grade': row['grade']} for row in res]
        return top_scores
    except DatabaseError as e:
        # Handle database query error
        raise DatabaseError("An error was occurred.") from e

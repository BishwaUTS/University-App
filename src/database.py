import os
import pickle

class Database:
    FILE_PATH = 'students.data'

    @classmethod
    def create_file_if_not_exists(cls):
        # Create file if it doesn't exist
        if not os.path.exists(cls.FILE_PATH):
            with open(cls.FILE_PATH, 'wb') as f:
                pickle.dump([], f)

    @classmethod
    def read_students(cls):
        # Read students from file
        cls.create_file_if_not_exists()
        with open(cls.FILE_PATH, 'rb') as f:
            try:
                return pickle.load(f)
            except EOFError:
                return []

    @classmethod
    def write_students(cls, students):
        # Write students to file
        with open(cls.FILE_PATH, 'wb') as f:
            pickle.dump(students, f)

    @classmethod
    def find_student_by_email(cls, email):
        # Find student by email
        students = cls.read_students()
        return next((student for student in students if student.email == email), None)

    @classmethod
    def clear_database(cls):
        # Clear all students from database
        with open(cls.FILE_PATH, 'wb') as f:
            pickle.dump([], f)
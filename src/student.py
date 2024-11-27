import random
import re

class Student:
    def __init__(self, name, email, password):
        # Generate unique 6-digit student ID
        self.id = str(random.randint(1, 999999)).zfill(6)
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []  # List to store enrolled subjects

    def enroll_subject(self, subject):
        # Check if student can enroll in more subjects
        if len(self.subjects) < 4:
            self.subjects.append(subject)
            return True
        return False

    def remove_subject(self, subject_id):
        # Remove subject by ID
        self.subjects = [subj for subj in self.subjects if subj.id != subject_id]

    def change_password(self, new_password, confirm_password):
        # Add password confirmation for changing password
        if self.validate_password(new_password)[0] and new_password == confirm_password:
            self.password = new_password
            return True
        return False

    def calculate_average_mark(self):
        # Calculate average mark across all subjects
        if not self.subjects:
            return 0
        return sum(subj.mark for subj in self.subjects) / len(self.subjects)

    @staticmethod
    def validate_email(email):
        # Validate email format
        pattern = r'^[a-zA-Z]+\.[a-zA-Z]+@university\.com$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password):
        # Comprehensive password validation with detailed error messages
        errors = []

        # Check password length
        if len(password) < 8:
            errors.append("❌ Password must be at least 8 characters long")

        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            errors.append("❌ Password must contain at least one uppercase letter")

        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            errors.append("❌ Password must contain at least one lowercase letter")

        # Check for digit
        if not re.search(r'\d', password):
            errors.append("❌ Password must contain at least one number")

        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("❌ Password must contain at least one special character")

        # Specific pattern validation
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$'
        is_valid = re.match(pattern, password) is not None

        return is_valid, errors

    def password_strength_feedback(password):
        # Provide strength feedback
        is_valid, errors = Student.validate_password(password)
        
        if is_valid:
            return "🟢 Strong Password!"
        
        strength_levels = {
            'weak': len(errors) > 3,
            'medium': len(errors) > 1 and len(errors) <= 3,
            'strong': len(errors) <= 1
        }
        
        if strength_levels['weak']:
            return "🔴 Weak Password - Major improvements needed!"
        elif strength_levels['medium']:
            return "🟠 Moderate Password - Some improvements required"
        else:
            return "🟡 Almost Strong - Close to a secure password!"
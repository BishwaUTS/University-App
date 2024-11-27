import random

class Subject:
    def __init__(self, subject_name):
        # Generate unique 3-digit subject ID
        self.id = str(random.randint(1, 999)).zfill(3)
        self.name = subject_name
        self.mark = random.randint(25, 100)
        self.grade = self._calculate_grade()

    def _calculate_grade(self):
        # Calculate grade based on mark
        if self.mark >= 85:
            return 'HD'
        elif self.mark >= 75:
            return 'D'
        elif self.mark >= 65:
            return 'C'
        elif self.mark >= 50:
            return 'P'
        else:
            return 'F'
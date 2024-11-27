from src.student import Student
from src.subject import Subject
from src.database import Database

class CLIUniApp:
    # Class-level list of available subjects
    AVAILABLE_SUBJECTS = [
        # Science Subjects
        'Biology', 'Chemistry', 'Physics', 'Environmental Science', 
        'Astronomy', 'Geology', 'Neuroscience',
        
        # Computer Science & Technology
        'Computer Science', 'Software Engineering', 'Cybersecurity', 
        'Artificial Intelligence', 'Data Science', 'Web Development', 
        'Network Engineering',
        
        # Engineering
        'Mechanical Engineering', 'Electrical Engineering', 
        'Civil Engineering', 'Chemical Engineering', 
        'Aerospace Engineering', 'Robotics Engineering',
        
        # Mathematics & Statistics
        'Mathematics', 'Applied Mathematics', 'Statistics', 
        'Actuarial Science', 'Financial Mathematics',
        
        # Business & Economics
        'Business Administration', 'Economics', 'Accounting', 
        'International Business', 'Marketing', 'Finance',
        
        # Social Sciences
        'Psychology', 'Sociology', 'Anthropology', 
        'Political Science', 'International Relations',
        
        # Humanities
        'History', 'Philosophy', 'Literature', 'Linguistics', 
        'Cultural Studies', 'Media Studies',
        
        # Health Sciences
        'Nursing', 'Public Health', 'Nutrition', 
        'Medical Laboratory Science', 'Pharmacy'
    ]

    @staticmethod
    def university_menu():
        while True:
            print("\n--- University System ---")
            print("(A) Admin")
            print("(S) Student")
            print("(X) Exit")
            choice = input("Enter your choice: ").lower()

            if choice == 'a':
                CLIUniApp.admin_system()
            elif choice == 's':
                CLIUniApp.student_system()
            elif choice == 'x':
                break
            else:
                print("Invalid choice. Try again.")

    @staticmethod
    def student_system():
        while True:
            print("\n--- Student System ---")
            print("(l) Login")
            print("(r) Register")
            print("(x) Exit")
            choice = input("Enter your choice: ").lower()

            if choice == 'l':
                CLIUniApp.login()
            elif choice == 'r':
                CLIUniApp.register()
            elif choice == 'x':
                break
            else:
                print("Invalid choice. Try again.")

    @staticmethod
    def register():
        print("\n🎓 STUDENT REGISTRATION 🎓")
        
        while True:
            # Collect registration details
            name = input("Enter your full name: ")
            email = input("Enter email (firstname.lastname@university.com): ")
            
            # Email validation
            if not Student.validate_email(email):
                print("❌ Invalid email format!")
                print("Email must be in format: firstname.lastname@university.com")
                continue

            # Password input with guidance
            while True:
                password = input("\nEnter password: ")
                
                # Validate password
                is_valid, errors = Student.validate_password(password)
                
                # Display strength feedback
                print(Student.password_strength_feedback(password))
                
                if is_valid:
                    break
                else:
                    print("\n🚨 PASSWORD DOES NOT MEET REQUIREMENTS:")
                    for error in errors:
                        print(error)
                    
                    retry = input("\nWould you like to try again? (y/n): ").lower()
                    if retry != 'y':
                        return
            
            # Final registration steps
            try:
                # Check if student already exists
                students = Database.read_students()
                if any(student.email == email for student in students):
                    print("❌ Student with this email already exists!")
                    continue

                # Create and save new student
                new_student = Student(name, email, password)
                students.append(new_student)
                Database.write_students(students)
                
                print(f"\n✅ Registration Successful!")
                print(f"🆔 Your Student ID is: {new_student.id}")
                break

            except Exception as e:
                print(f"❌ Registration failed: {e}")

    @staticmethod
    def login():
        print("\n--- Student Login ---")
        email = input("Enter email: ")
        password = input("Enter password: ")

        student = Database.find_student_by_email(email)
        if student and student.password == password:
            CLIUniApp.subject_enrollment_system(student)
        else:
            print("Invalid credentials!")

    @staticmethod
    def subject_enrollment_system(student):
        while True:
            print("\n--- Subject Enrollment System ---")
            print("Current Subjects:", len(student.subjects), "/4")
            print("(e) Enroll in Subject")
            print("(r) Remove Subject")
            print("(s) Show Subjects")
            print("(c) Change Password")
            print("(x) Exit")
            
            choice = input("Enter your choice: ").lower()

            if choice == 'e':
                # Improved subject enrollment
                if len(student.subjects) >= 4:
                    print("❌ Maximum subject limit (4) reached!")
                    input("Press Enter to continue...")
                    continue

                # Display available subjects with pagination
                while True:
                    print("\n--- Available Subjects ---")
                    for i in range(0, len(CLIUniApp.AVAILABLE_SUBJECTS), 10):
                        page = CLIUniApp.AVAILABLE_SUBJECTS[i:i+10]
                        for j, sub in enumerate(page, 1):
                            print(f"{i+j}. {sub}")
                        
                        # Pagination control
                        if i + 10 < len(CLIUniApp.AVAILABLE_SUBJECTS):
                            next_page = input("Enter 'n' for next page or 'x' to exit: ").lower()
                            if next_page == 'n':
                                continue
                            elif next_page == 'x':
                                break
                        
                        # Subject selection
                        try:
                            sub_choice = int(input("Choose subject number: "))
                            if 1 <= sub_choice <= len(CLIUniApp.AVAILABLE_SUBJECTS):
                                selected_subject = CLIUniApp.AVAILABLE_SUBJECTS[sub_choice - 1]
                                
                                # Check if subject already enrolled
                                if any(sub.name == selected_subject for sub in student.subjects):
                                    print(f"❌ You are already enrolled in {selected_subject}!")
                                    input("Press Enter to continue...")
                                    break
                                
                                # Create and enroll subject
                                new_subject = Subject(selected_subject)
                                if student.enroll_subject(new_subject):
                                    print(f"✅ Enrolled in {new_subject.name}")
                                    print(f"Subject ID: {new_subject.id}")
                                    print(f"Marks: {new_subject.mark}")
                                    print(f"Grade: {new_subject.grade}")
                                    input("Press Enter to continue...")
                                    break
                                else:
                                    print("❌ Could not enroll in subject")
                                    input("Press Enter to continue...")
                                    break
                            else:
                                print("Invalid subject number!")
                        except ValueError:
                            print("Please enter a valid number!")
                    break

            elif choice == 'r':
                if not student.subjects:
                    print("❌ No subjects to remove!")
                    input("Press Enter to continue...")
                    continue
                
                print("--- Current Subjects ---")
                for sub in student.subjects:
                    print(f"ID: {sub.id}, Name: {sub.name}, Mark: {sub.mark}, Grade: {sub.grade}")
                
                sub_id = input("Enter subject ID to remove: ")
                student.remove_subject(sub_id)
                print("✅ Subject removed!")
                input("Press Enter to continue...")

            elif choice == 's':
                if not student.subjects:
                    print("❌ No subjects enrolled!")
                    input("Press Enter to continue...")
                    continue
                
                print("\n--- Enrolled Subjects ---")
                for sub in student.subjects:
                    print(f"ID: {sub.id}, Name: {sub.name}, Mark: {sub.mark}, Grade: {sub.grade}")
                print(f"Average Mark: {student.calculate_average_mark():.2f}")
                input("Press Enter to continue...")

            elif choice == 'c':
                # Password change with validation
                current_password = input("Enter current password: ")
                
                # Verify current password
                if current_password != student.password:
                    print("❌ Incorrect current password!")
                    input("Press Enter to continue...")
                    continue
                
                new_password = input("Enter new password: ")
                
                # Validate new password
                is_valid, errors = Student.validate_password(new_password)
                
                if is_valid:
                    confirm_password = input("Confirm new password: ")
                    
                    if student.change_password(new_password, confirm_password):
                        print("✅ Password changed successfully!")
                    else:
                        print("❌ Password change failed. Passwords do not match.")
                else:
                    print("\n🚨 NEW PASSWORD DOES NOT MEET REQUIREMENTS:")
                    for error in errors:
                        print(error)
                
                input("Press Enter to continue...")

            elif choice == 'x':
                # Save student data before exiting
                students = Database.read_students()
                for i, existing_student in enumerate(students):
                    if existing_student.email == student.email:
                        students[i] = student
                        break
                Database.write_students(students)
                break

            else:
                print("Invalid choice. Try again.")
                input("Press Enter to continue...")

    @staticmethod
    def admin_system():
        while True:
            print("\n--- Admin System ---")
            print("(s) Show Students")
            print("(g) Group Students")
            print("(p) Partition Students")
            print("(r) Remove Student")
            print("(c) Clear Database")
            print("(x) Exit")
            
            choice = input("Enter your choice: ").lower()

            students = Database.read_students()

            if choice == 's':
                if not students:
                    print("No students in database!")
                    continue
                for student in students:
                    print(f"ID: {student.id}, Name: {student.name}, Email: {student.email}")

            elif choice == 'g':
                # Group students by grade average
                students.sort(key=lambda s: s.calculate_average_mark(), reverse=True)
                for student in students:
                    print(f"Student: {student.name}, Average Mark: {student.calculate_average_mark():.2f}")

            elif choice == 'p':
                # Partition students to PASS/FAIL
                pass_students = [s for s in students if s.calculate_average_mark() >= 50]
                fail_students = [s for s in students if s.calculate_average_mark() < 50]
                
                print("--- Pass Students ---")
                for student in pass_students:
                    print(f"ID: {student.id}, Name: {student.name}, Average Mark: {student.calculate_average_mark():.2f}")
                
                print("\n--- Fail Students ---")
                for student in fail_students:
                    print(f"ID: {student.id}, Name: {student.name}, Average Mark: {student.calculate_average_mark():.2f}")

            elif choice == 'r':
                student_id = input("Enter student ID to remove: ")
                students = [s for s in students if s.id != student_id]
                Database.write_students(students)
                print("Student removed!")

            elif choice == 'c':
                Database.clear_database()
                print("Database cleared!")

            elif choice == 'x':
                break

if __name__ == "__main__":
    CLIUniApp.university_menu()
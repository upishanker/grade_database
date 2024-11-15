from user import User
from course import Course
from assignment import Assignment
from session import Session
from tabulate import tabulate

class Menu:
    def __init__(self):
        self.session = Session.get_instance()
    def add_course(self, user_id):
        """Add a new course."""
        try:
            name = input("\nEnter course name: ").strip()
            if not name:
                print("Course name cannot be empty.")
                return
            hours = input("Enter credit hours: ").strip()
            if not hours.isdigit():
                print("Credit hours must be a positive number.")
                return
                
            course = Course(name, int(hours), user_id=user_id)
            course.save()
            
        except Exception as e:
            print(f"Error adding course: {e}")

    def add_assignment(self, user_id):
        """Add a new assignment to a course."""
        course = Course.choose_course(user_id, True)
        if not course:
            return
        try:
            name = input("\nEnter assignment name: ").strip()
            if not name:
                print("Assignment name cannot be empty.")
                return

            weight = input("Enter assignment weight (percentage): ").strip()
            try:
                weight = float(weight)
                if weight <= 0 or weight > 100:
                    print("Weight must be between 0 and 100.")
                    return
            except ValueError:
                print("Weight must be a number.")
                return

            grade_input = input("Enter grade (-1 if not graded yet): ").strip()
            try:
                grade = float(grade_input)
                if grade != -1 and (grade < 0 or grade > 100):
                    print("Grade must be between 0 and 100 (or -1 for not graded).")
                    return
            except ValueError:
                print("Grade must be a number.")
                return

            assignment = Assignment(name, weight, grade, course_id=course.course_id)
            assignment.save()

        except Exception as e:
            print(f"Error adding assignment: {e}")

    def remove_course(self, user_id):
        """Remove a course and all its assignments."""
        course = Course.choose_course(user_id, True)
        if course:
            confirm = input(f"\nAre you sure you want to delete '{course.name}' and all its assignments? (y/n): ")
            while confirm.lower() != 'y' or confirm.lower() != 'n':
                print("Please enter y or n")
                confirm = input(f"\nAre you sure you want to delete '{course.name}' and all its assignments? (y/n): ")
            if confirm.lower() == 'y':
                course.remove()
            
    def remove_assignment(self, user_id):
        """Remove an assignment from a course."""
        course = Course.choose_course(user_id, True)
        if not course:
            return

        assignments = Assignment.get_course_assignments(course.course_id)
        if not assignments:
            print("\nNo assignments found for this course.")
            return

        # Display assignments
        headers = ["#", "Assignment Name", "Weight (%)", "Grade"]
        table_data = []
        for idx, (assignment_id, name, weight, grade) in enumerate(assignments, 1):
            grade_display = f"{grade:.2f}" if grade is not None else "Not graded"
            table_data.append([idx, name, f"{weight:.2f}", grade_display])

        print("\nSelect assignment to remove:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        try:
            choice = input("\nEnter the number of the assignment to remove (0 to cancel): ")
            if choice.strip() == "0":
                return

            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(assignments):
                assignment_id, name, weight, grade = assignments[choice_idx]
                assignment = Assignment(name, weight, grade, assignment_id, course.course_id)
                
                confirm = input(f"\nAre you sure you want to delete '{name}'? (y/n): ")
                if confirm.lower() == 'y':
                    assignment.remove()
            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error removing assignment: {e}")

    def list_courses(self, user_id):
        """List all courses and their grades."""
        Course.choose_course(user_id, False)

    def list_assignments(self, user_id):
        """List all assignments for a selected course."""
        course = Course.choose_course(user_id, True)
        if course:
            Assignment.list_assignments(course.course_id)

    def main_menu(self):
        """Display and handle the main menu."""
        current_user = self.session.get_current_user()
        
        while True:
            print("\nGrade Calculator Menu")
            print("1: Add Course")
            print("2: Add Assignment")
            print("3: Remove Course")
            print("4: Remove Assignment")
            print("5: List Courses")
            print("6: List Assignments")
            print("7: Logout")
            print("0: Exit")

            choice = input("\nChoose an option: ")

            if choice == "0":
                return False
            elif choice == "7":
                self.session.logout()
                print("\nLogged out successfully")
                return True

            # Menu options that require a logged-in user
            options = {
                "1": self.add_course,
                "2": self.add_assignment,
                "3": self.remove_course,
                "4": self.remove_assignment,
                "5": self.list_courses,
                "6": self.list_assignments
            }

            if choice in options:
                options[choice](current_user.user_id)
            else:
                print("\nInvalid option. Please try again.")

    def login_menu(self):
        """Display and handle the login menu."""
        while True:
            print("\nWelcome to Grade Calculator!")
            print("1: Login")
            print("2: Register")
            print("0: Exit")
            
            choice = input("\nChoose an option: ")
            
            if choice == "0":
                return False
                
            elif choice == "1":
                username = input("Username: ")
                password = input("Password: ")
                user = User.authenticate(username, password)
                if user:
                    self.session.login(user)
                    print(f"\nWelcome back, {username}!")
                    return True
                else:
                    print("\nInvalid username or password")
                    
            elif choice == "2":
                username = input("Choose a username: ")
                password = input("Choose a password: ")
                user = User.create_user(username, password)
                if user:
                    print("\nUser created successfully! Please login.")
                else:
                    print("\nUsername already exists")
            else:
                print("\nInvalid option. Please try again.")

    def start(self):
        """Start the menu system."""
        while True:
            if self.login_menu():
                should_continue = self.main_menu()
                if not should_continue:
                    break
            else:
                break
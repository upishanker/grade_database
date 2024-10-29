from student import Student
from course import Course
from assignment import Assignment
from settings import students
def menu():
    print("Welcome to Grade Calculator! Please select a menu option")
    print("1: Add Student")
    print("2: Add Course")
    print("3: Add Assignment")
    print("4: Remove Course")
    print("5: Remove Assignment")
    print("6: List Students")
    print("7: List Courses")
    print("8: List Assignments")
    choice = input("Choose an option: (Enter 0 to exit): ")
    if choice == "0":
        exit()
    if choice == "1":
        name = input("Enter Student Name: ")
        students.append(Student(name))
        menu()
    if choice == "2":
            student = Student.choose_student()
            if student == -1:
                menu()
            coursename = input("Enter Course Name: ")
            coursehours = input("Enter Course Hours: ")
            students[student].add_course(Course(coursename, coursehours))
            menu()
    if choice == "3":
        student = Student.choose_student()
        if student == -1:
            menu()
        course = Course.choose_course(student)
        if course == -1:
            menu()
        assignmentname = input("Enter Assignment Name: ")
        assignmentgrade = input("Enter Assignment Grade: (enter -1 if not graded): ")
        assignmentweight = input("Enter Assignment Weight (percentage): ")
        students[student].courses[course].add_assignment(Assignment(assignmentname, assignmentweight, assignmentgrade))
        menu()
    if choice == "4":
        student = Student.choose_student()
        if student == -1:
            menu()
        else:
            course = Course.choose_course(student)
            if course == -1:
                menu()
            else:
                students[student].remove_course(course)
                menu()
    if choice == "5":
        student = Student.choose_student()
        if student == -1:
            menu()
        else:
            course = Course.choose_course(student)
            if course == -1:
                menu()
            else:
                assignment = Assignment.choose_assignment(student, course)
                students[student].courses[course].remove_assignment(assignment)
                menu()
    if choice == "6":
        Student.choose_student()
        menu()
    if choice == "7":
        student = Student.choose_student()
        if student == -1:
            menu()
        else:
            Course.choose_course(student)
            menu()
    if choice == "8":
        student = Student.choose_student()
        if student == -1:
            menu()
        else:
            Assignment.choose_assignment(student, Course.choose_course(student))
            menu()





        
                                


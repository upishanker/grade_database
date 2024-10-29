from settings import students
class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def remove_course(self, course_number):
        self.courses = [course for course in self.courses if course.name != self.courses[course_number].name]

    def choose_student():
        print("Choose a Student")
        if not students:
            print("\nNo students: Please add a student\n")
            return -1
        for i in range(len(students)):
            print(f"{i}: {students[i].name}")
        return int(input(""))
    
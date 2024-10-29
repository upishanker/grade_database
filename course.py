from settings import students
class Course:
    def __init__(self, name, hours):
        self.name = name
        self.hours = hours
        self.assignments = []

    def add_assignment(self, assignment):
        self.assignments.append(assignment)

    def remove_assignment(self, assignment_number):
        self.assignments = [a for a in self.assignments if a.name != self.assignments[assignment_number].name]

    def calculate_current_grade(self):
        current_grade = sum([a.grade * a.weight for a in self.assignments])
        return current_grade

    def choose_course(student):
        if not students[student].courses:
            print("\nNo courses: Please add a course\n")
            return -1
        print("Choose a Course")
        for i in range(len(students[student].courses)):
            print(f"{i}: {students[student].courses[i].name}")
        return int(input(""))
    
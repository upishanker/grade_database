from settings import students
class Assignment:
    def __init__(self, name, weight, grade):
        self.name = name
        self.weight = weight
        self.grade = grade
    def choose_assignment(student, course):
        print("Choose an assignment: ")
        for i in range(len(students[student].courses[course].assignments)):
            print(f"{i}: {students[student].courses[course].assignments[i].name}")
        return int(input(""))

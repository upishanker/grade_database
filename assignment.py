from database import connect_db, get_cursor
from tabulate import tabulate

class Assignment:
    def __init__(self, name, weight, grade=None, assignment_id=None, course_id=None):
        self.name = name
        self.weight = weight
        self.grade = grade if grade != -1 else None
        self.assignment_id = assignment_id
        self.course_id = course_id

    @staticmethod
    def get_course_assignments(course_id):
        """Get all assignments for a specific course."""
        conn = connect_db()
        cursor = get_cursor(conn)
        
        query = """
        SELECT 
            id,
            name,
            weight,
            grade
        FROM assignments
        WHERE course_id = ?
        ORDER BY name
        """
        
        try:
            cursor.execute(query, (course_id,))
            assignments = cursor.fetchall()
            conn.close()
            return assignments
        except Exception as e:
            print(f"Database error: {e}")
            conn.close()
            return []

    @staticmethod
    def list_assignments(course_id, option=False):
        """Display all assignments for a course."""
        assignments = Assignment.get_course_assignments(course_id)
        
        if not assignments:
            print("\nNo assignments found for this course.")
            return

        # Prepare data for tabulate
        headers = ["#", "Assignment Name", "Weight (%)", "Grade"]
        table_data = []
        
        total_weight = 0
        weighted_grade = 0
        
        for idx, (assignment_id, name, weight, grade) in enumerate(assignments, 1):
            grade_display = f"{grade:.2f}" if grade is not None else "Not graded"
            table_data.append([idx, name, f"{weight:.2f}", grade_display])
            

        # Print formatted table
        print("\nAssignments:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        while option:
            try:
                choice = input("\nEnter the number of the assignment (0 to cancel): ")
                
                if choice.strip() == "0":
                    return None
                
                choice_idx = int(choice) - 1
                
                if 0 <= choice_idx < len(assignments):
                    course_id, name, hours, _ = assignments[choice_idx]
                    return Assignment(name, hours, course_id)
                else:
                    print("Invalid choice. Please try again.")
            
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

    def save(self):
        """Save or update the assignment in the database."""
        conn = connect_db()
        cursor = get_cursor(conn)
        
        try:
            if self.assignment_id is None:
                # New assignment
                cursor.execute(
                    "INSERT INTO assignments (name, weight, grade, course_id) VALUES (?, ?, ?, ?)",
                    (self.name, self.weight, self.grade, self.course_id)
                )
                self.assignment_id = cursor.lastrowid
            else:
                # Update existing assignment
                cursor.execute(
                    "UPDATE assignments SET name = ?, weight = ?, grade = ? WHERE id = ?",
                    (self.name, self.weight, self.grade, self.assignment_id)
                )
            
            conn.commit()
            print(f"\nAssignment '{self.name}' {'added' if cursor.rowcount > 0 else 'updated'} successfully!")
            
        except Exception as e:
            conn.rollback()
            print(f"Error saving assignment: {e}")
        finally:
            conn.close()

    def update(self, option):
        conn = connect_db()
        cursor = get_cursor(conn)
        if option == "1":
            name = input("Enter the new name: ")
            try:
                cursor.execute("UPDATE assignments SET name = ? WHERE id = ?", (name, self.assignment_id))
            except Exception as e:
                conn.rollback()
                print(f"Error updating name: {e}")
        if option == "2":
            grade = input("Enter the new grade: ")
            try:
                cursor.execute("UPDATE assignments SET grade = ? WHERE id = ?", (grade, self.assignment_id))
            except Exception as e:
                conn.rollback()
                print(f"Error updating grade: {e}")
        if option == "3":
            weight = input("Enter the new weight: ")
            try:
                cursor.execute("UPDATE assignments SET weight = ? WHERE id = ?", (weight, self.assignment_id))
            except Exception as e:
                conn.rollback()
                print(f"Error updating weight: {e}")
        conn.commit()
        conn.close()
    def remove(self):
        """Remove the assignment from the database."""
        conn = connect_db()
        cursor = get_cursor(conn)
        
        try:
            cursor.execute(
                "DELETE FROM assignments WHERE id = ?",
                (self.assignment_id,)
            )
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"\nAssignment '{self.name}' deleted successfully!")
            else:
                print("\nAssignment not found.")
                
        except Exception as e:
            conn.rollback()
            print(f"Error deleting assignment: {e}")
        finally:
            conn.close()
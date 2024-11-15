from database import connect_db, get_cursor
from tabulate import tabulate  # Add this to requirements.txt

class Course:
    def __init__(self, name, hours, course_id=None, user_id=None):
        self.name = name
        self.hours = hours
        self.course_id = course_id
        self.user_id = user_id

    @staticmethod
    def get_user_courses(user_id):
        """Get all courses for a specific user with their current grades."""
        conn = connect_db()
        cursor = get_cursor(conn)
        
        # Query to get courses with their current total grade
        query = """
        SELECT 
            c.id,
            c.name,
            c.hours,
            COUNT(a.id) as assignment_count
        FROM courses c
        LEFT JOIN assignments a ON c.id = a.course_id
        WHERE c.user_id = ?
        GROUP BY c.id, c.name, c.hours
        ORDER BY c.name
        """
        
        try:
            cursor.execute(query, (user_id,))
            courses = cursor.fetchall()
            conn.close()
            return courses
        except Exception as e:
            print(f"Database error: {e}")
            conn.close()
            return []

    @staticmethod
    def choose_course(user_id, option):
        """Display courses and let user choose one."""
        courses = Course.get_user_courses(user_id)
        
        if not courses:
            print("\nNo courses found. Please add a course first.")
            return None
        # Prepare data for tabulate
        headers = ["#", "Course Name", "Credit Hours", "Current Grade", "Assignments"]
        table_data = []
        
        for idx, (course_id, name, hours, assignment_count) in enumerate(courses, 1):
            # Format current grade to 2 decimal places if it exists
            current_grade = Course.calculate_current_grade(course_id)
            grade_display = f"{current_grade:.2f}%" if current_grade is not None else "N/A"
            
            table_data.append([
                idx,
                name,
                hours,
                grade_display,
                assignment_count
            ])

        # Print formatted table
        print("\nYour Courses:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Get user choice
        while option:
            try:
                choice = int(input("\nEnter the number of the course (0 to cancel): "))
                
                if choice == 0:
                    return None
                
                choice_idx = choice - 1
                
                if 0 <= choice_idx < len(courses):
                    course_id, name, hours, _ = courses[choice_idx]
                    return Course(name, hours, course_id, user_id)
                else:
                    print("Invalid choice. Please try again.")
            
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

    def save(self):
        """Save or update the course in the database."""
        conn = connect_db()
        cursor = get_cursor(conn)
        
        try:
            if self.course_id is None:
                # New course
                cursor.execute(
                    "INSERT INTO courses (name, hours, user_id) VALUES (?, ?, ?)",
                    (self.name, self.hours, self.user_id)
                )
                self.course_id = cursor.lastrowid
            else:
                # Update existing course
                cursor.execute(
                    "UPDATE courses SET name = ?, hours = ? WHERE id = ? AND user_id = ?",
                    (self.name, self.hours, self.course_id, self.user_id)
                )
            
            conn.commit()
            print(f"\nCourse '{self.name}' {'added' if cursor.rowcount > 0 else 'updated'} successfully!")
            
        except Exception as e:
            conn.rollback()
            print(f"Error saving course: {e}")
        finally:
            conn.close()

    def remove(self):
        """Remove the course and its assignments from the database."""
        conn = connect_db()
        cursor = get_cursor(conn)
        
        try:
            # Begin transaction
            conn.execute("BEGIN TRANSACTION")
            
            # Delete assignments first
            cursor.execute(
                "DELETE FROM assignments WHERE course_id = ?",
                (self.course_id,)
            )
            assignments_deleted = cursor.rowcount
            
            # Then delete the course
            cursor.execute(
                "DELETE FROM courses WHERE id = ? AND user_id = ?",
                (self.course_id, self.user_id)
            )
            
            if cursor.rowcount > 0:
                conn.commit()
                print(f"\nCourse '{self.name}' and {assignments_deleted} assignment(s) deleted successfully!")
            else:
                conn.rollback()
                print("\nCourse not found or you don't have permission to delete it.")
                
        except Exception as e:
            conn.rollback()
            print(f"Error deleting course: {e}")
        finally:
            conn.close()

    @staticmethod
    def calculate_current_grade(course_id):
        """Calculate the current grade for the course."""
        conn = connect_db()
        cursor = get_cursor(conn)

        try:
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(grade * weight), 0) as total_grade,
                    COALESCE(SUM(weight), 0) as total_weight
                FROM assignments
                WHERE course_id = ? AND grade IS NOT NULL AND grade != -1
            """, (course_id,))
            
            result = cursor.fetchone()
            if result:
                total_grade = result[0]
                total_weight = result[1]
                if total_weight == 0:
                    return 0
                return total_grade / total_weight
            else:
                return 0
            
        except Exception as e:
            print(f"Error calculating grade: {e}")
            return 0
        finally:
            conn.close()
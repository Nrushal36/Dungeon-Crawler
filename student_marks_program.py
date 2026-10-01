"""
Student Marks Program
This program allows you to manage and calculate student marks.
Features:
- Add students and their marks
- Calculate average marks
- Find highest and lowest marks
- Display student report
"""

class StudentMarksProgram:
    """A class to manage student marks."""
    
    def __init__(self):
        """Initialize the student marks database."""
        self.students = {}
    
    def add_student(self, name, marks):
        """
        Add a student with their marks.
        
        Args:
            name (str): Student's name
            marks (list or float): Marks obtained (can be single mark or list of marks)
        """
        if isinstance(marks, (list, tuple)):
            self.students[name] = list(marks)
        else:
            self.students[name] = [marks]
        print(f"✓ Student '{name}' added successfully with marks: {self.students[name]}")
    
    def calculate_average(self, name):
        """
        Calculate average marks for a student.
        
        Args:
            name (str): Student's name
            
        Returns:
            float: Average marks or None if student not found
        """
        if name not in self.students:
            print(f"✗ Student '{name}' not found.")
            return None
        
        marks = self.students[name]
        average = sum(marks) / len(marks)
        return round(average, 2)
    
    def get_highest_marks(self, name):
        """
        Get the highest mark for a student.
        
        Args:
            name (str): Student's name
            
        Returns:
            float: Highest mark or None if student not found
        """
        if name not in self.students:
            print(f"✗ Student '{name}' not found.")
            return None
        
        return max(self.students[name])
    
    def get_lowest_marks(self, name):
        """
        Get the lowest mark for a student.
        
        Args:
            name (str): Student's name
            
        Returns:
            float: Lowest mark or None if student not found
        """
        if name not in self.students:
            print(f"✗ Student '{name}' not found.")
            return None
        
        return min(self.students[name])
    
    def get_total_marks(self, name):
        """
        Get total marks for a student.
        
        Args:
            name (str): Student's name
            
        Returns:
            float: Total marks or None if student not found
        """
        if name not in self.students:
            print(f"✗ Student '{name}' not found.")
            return None
        
        return sum(self.students[name])
    
    def get_grade(self, name):
        """
        Calculate grade based on average marks.
        
        Grading Scale:
        A: 90-100
        B: 80-89
        C: 70-79
        D: 60-69
        F: Below 60
        
        Args:
            name (str): Student's name
            
        Returns:
            str: Grade or None if student not found
        """
        average = self.calculate_average(name)
        
        if average is None:
            return None
        
        if average >= 90:
            return 'A'
        elif average >= 80:
            return 'B'
        elif average >= 70:
            return 'C'
        elif average >= 60:
            return 'D'
        else:
            return 'F'
    
    def display_student_report(self, name):
        """
        Display a detailed report for a student.
        
        Args:
            name (str): Student's name
        """
        if name not in self.students:
            print(f"✗ Student '{name}' not found.")
            return
        
        marks = self.students[name]
        average = self.calculate_average(name)
        grade = self.get_grade(name)
        
        print(f"\n{'='*50}")
        print(f"{'STUDENT MARKS REPORT':^50}")
        print(f"{'='*50}")
        print(f"Name           : {name}")
        print(f"Marks          : {marks}")
        print(f"Total Marks    : {self.get_total_marks(name)}")
        print(f"Average Marks  : {average}")
        print(f"Highest Marks  : {self.get_highest_marks(name)}")
        print(f"Lowest Marks   : {self.get_lowest_marks(name)}")
        print(f"Grade          : {grade}")
        print(f"{'='*50}\n")
    
    def display_all_students(self):
        """Display marks for all students."""
        if not self.students:
            print("✗ No students in the database.")
            return
        
        print(f"\n{'='*70}")
        print(f"{'ALL STUDENTS MARKS':^70}")
        print(f"{'='*70}")
        print(f"{'Name':<20} {'Marks':<20} {'Average':<10} {'Grade':<10}")
        print(f"{'-'*70}")
        
        for name in self.students:
            average = self.calculate_average(name)
            grade = self.get_grade(name)
            print(f"{name:<20} {str(self.students[name]):<20} {average:<10} {grade:<10}")
        
        print(f"{'='*70}\n")
    
    def delete_student(self, name):
        """
        Delete a student from the database.
        
        Args:
            name (str): Student's name
        """
        if name in self.students:
            del self.students[name]
            print(f"✓ Student '{name}' deleted successfully.")
        else:
            print(f"✗ Student '{name}' not found.")


def main():
    """Main function to run the Student Marks Program."""
    program = StudentMarksProgram()
    
    while True:
        print("\n" + "="*50)
        print("STUDENT MARKS MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Student")
        print("2. View Student Report")
        print("3. View All Students")
        print("4. Calculate Average")
        print("5. Get Grade")
        print("6. Delete Student")
        print("7. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            name = input("Enter student name: ").strip()
            try:
                marks_input = input("Enter marks (comma-separated if multiple subjects): ").strip()
                marks = [float(x.strip()) for x in marks_input.split(',')]
                program.add_student(name, marks)
            except ValueError:
                print("✗ Invalid input! Please enter numeric values for marks.")
        
        elif choice == '2':
            name = input("Enter student name: ").strip()
            program.display_student_report(name)
        
        elif choice == '3':
            program.display_all_students()
        
        elif choice == '4':
            name = input("Enter student name: ").strip()
            average = program.calculate_average(name)
            if average is not None:
                print(f"Average marks for {name}: {average}")
        
        elif choice == '5':
            name = input("Enter student name: ").strip()
            grade = program.get_grade(name)
            if grade is not None:
                print(f"Grade for {name}: {grade}")
        
        elif choice == '6':
            name = input("Enter student name: ").strip()
            program.delete_student(name)
        
        elif choice == '7':
            print("Thank you for using Student Marks Management System!")
            break
        
        else:
            print("✗ Invalid choice! Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()

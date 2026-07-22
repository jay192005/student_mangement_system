from database.db import Database
from models.student import Student
from utils.id_generator import generate_id
import datetime

class StudentManagementSystem:

    def __init__(self):

        # self.students = []
        self.db = Database()

    def register_student(self, student):

        # self.students.append(student)
        query = """
        INSERT INTO students
        (
            student_id,
            name,
            email,
            mobile,
            course,
            gender,
            date_of_birth,
            address
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            student.student_id,
            student.name,
            student.email,
            student.mobile,
            student.course,
            student.gender,
            student.date_of_birth,
            student.address
        )

        self.db.execute(query, values)

        print("\nStudent Registered Successfully")

    # def view_students(self):

    #     if len(self.students) == 0:
    #         print("\nNo Students Found")
    #         return

    #     print("\n===== STUDENT LIST =====")

    #     for student in self.students:
    #         student.display()


    def view_students(self):

        query = "SELECT * FROM students"

        students = self.db.fetch_all(query)

        if not students:
            print("\nNo Students Found")
            return

        print("\n===== STUDENT LIST =====")

        for student in students:

            print("\n----- Student Details -----")

            print(f"Student ID     : {student['student_id']}")
            print(f"Name           : {student['name']}")
            print(f"Email          : {student['email']}")
            print(f"Mobile         : {student['mobile']}")
            print(f"Course         : {student['course']}")
            print(f"Gender         : {student['gender']}")
            print(f"Date Of Birth  : {student['date_of_birth']}")
            print(f"Address        : {student['address']}")

    # Helper Funtion to Search student

    # def find_student_by_id(self, student_id):

    #     for student in self.students:

    #         if student.student_id == student_id:
    #             return student

    #     return None

    def find_student_by_id(self, student_id):

        query = """
        SELECT *
        FROM students
        WHERE student_id = %s
        """

        return self.db.fetch_one(
            query,
            (student_id,)
        )

    # def search_student(self, student_id):

    #     student = self.find_student_by_id(student_id)

    #     if student:
    #         print("\nStudent Found")
    #         student.display()
    #         return
    #     else:
    #         print("Student Not Found!!")


    def search_student(self, student_id):

        student = self.find_student_by_id(student_id)

        if student:
            print("\nStudent Found")

            print("\n----- Student Details -----")

            print(f"Student ID     : {student['student_id']}")
            print(f"Name           : {student['name']}")
            print(f"Email          : {student['email']}")
            print(f"Mobile         : {student['mobile']}")
            print(f"Course         : {student['course']}")
            print(f"Gender         : {student['gender']}")
            print(f"Date Of Birth  : {student['date_of_birth']}")
            print(f"Address        : {student['address']}")

        else:
            print("\nStudent Not Found")

    def update_student(self, student_id):

        student = self.find_student_by_id(student_id)

        if student:

            print("\nLeave blank if you don't want to update.")

            name = input("Enter New Name: ").strip()
            
            while True:
                email = input("Enter New Email: ").strip()
                if not email or ("@" in email and "." in email):
                    break
                print("Invalid email! Please enter a valid email.")

            while True:
                mobile = input("Enter New Mobile: ").strip()
                if not mobile or (mobile.isdigit() and len(mobile) == 10):
                    break
                print("Invalid mobile! Please enter a 10-digit number.")

            course = input("Enter New Course: ").strip()
            
            while True:
                gender = input("Enter New Gender (male/female/other): ").strip().lower()
                if not gender or gender in ['male', 'female', 'other']:
                    break
                print("Invalid gender! Please enter male, female, or other.")

            while True:
                dob = input("Enter New DOB (YYYY-MM-DD): ").strip()
                if not dob:
                    break
                try:
                    datetime.datetime.strptime(dob, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format! Please enter in YYYY-MM-DD format.")

            address = input("Enter New Address: ").strip()

            # if name:
            #     student.name = name

            # if email:
            #     student.email = email

            # if mobile:
            #     student.mobile = mobile

            # if course:
            #     student.course = course

            # if gender:
            #     student.gender = gender

            # if dob:
            #     student.date_of_birth = dob

            # if address:
            #     student.address = address

            # Keep old values if user presses Enter

            name = name if name else student['name']

            email = email if email else student['email']

            mobile = mobile if mobile else student['mobile']

            course = course if course else student['course']

            gender = gender if gender else student['gender']

            dob = dob if dob else student['date_of_birth']

            address = address if address else student['address']


            query = """
            UPDATE students
            SET
                name = %s,
                email = %s,
                mobile = %s,
                course = %s,
                gender = %s,
                date_of_birth = %s,
                address = %s
            WHERE student_id = %s
            """

            values = (
                name,
                email,
                mobile,
                course,
                gender,
                dob,
                address,
                student_id
            )

            self.db.execute(query, values)

            print("\nStudent Updated Successfully")

        else:
            print("\nStudent Not Found")

    def update_student_academic_information(self, student_id, course):
        """Update the currently stored academic field for an authorized workflow.

        The Phase 1 schema stores a student's course as academic information.
        Marks, attendance, and subjects can be added later without changing the
        role authorization API.
        """
        if not self.find_student_by_id(student_id):
            raise ValueError("Student not found.")

        if not course or not course.strip():
            raise ValueError("Course cannot be empty.")

        self.db.execute(
            "UPDATE students SET course = %s WHERE student_id = %s",
            (course.strip(), student_id),
        )
        print("\nStudent Academic Information Updated Successfully")

    # def delete_student(self, student_id):

    #     student = self.find_student_by_id(student_id)

    #     print("Delete Test : \n", student)

    #     if student:

    #         self.students.remove(student)
    #         print("Student Deleted")

    #     else:
    #         print("Student Not Found!!")

    def delete_student(self, student_id):

        student = self.find_student_by_id(student_id)

        if student:

            query = """
            DELETE FROM students
            WHERE student_id = %s
            """

            self.db.execute(
                query,
                (student_id,)
            )

            print("\nStudent Deleted Successfully")

        else:

            print("\nStudent Not Found")

    def menu(self):

        while True:

            print("\n==============================")
            print(" STUDENT MANAGEMENT SYSTEM ")
            print("==============================")
            print("1. Register Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Exit")

            choice = input("\nEnter Your Choice: ")

            if choice == "1":

                existing_ids = [
                    student['student_id']
                    for student in self.db.fetch_all("SELECT student_id FROM students")
                ]
                student_id = generate_id("STU", existing_ids)
                print(f"Generated Student ID: {student_id}")

                # student_id = input("Enter Student ID: ")

                while True:
                    name = input("Enter Name: ").strip()
                    if name:
                        break
                    print("Name cannot be empty!")

                while True:
                    email = input("Enter Email: ").strip()
                    if "@" in email and "." in email:
                        break
                    print("Invalid email! Please enter a valid email.")

                while True:
                    mobile = input("Enter Mobile: ").strip()
                    if mobile.isdigit() and len(mobile) == 10:
                        break
                    print("Invalid mobile! Please enter a 10-digit number.")

                while True:
                    course = input("Enter Course: ").strip()
                    if course:
                        break
                    print("Course cannot be empty!")

                while True:
                    gender = input("Enter Gender (male/female/other): ").strip().lower()
                    if gender in ['male', 'female', 'other']:
                        break
                    print("Invalid gender! Please enter male, female, or other.")

                while True:
                    date_of_birth = input("Enter DOB (YYYY-MM-DD): ").strip()
                    try:
                        datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date format! Please enter in YYYY-MM-DD format.")

                while True:
                    address = input("City and State: ").strip()
                    if address:
                        break
                    print("Address cannot be empty!")

                student = Student(
                    student_id,
                    name,
                    email,
                    mobile,
                    course,
                    gender,
                    date_of_birth,
                    address
                )

                self.register_student(student)

            elif choice == "2":

                self.view_students()

            elif choice == "3":

                student_id = input("Enter Student ID: ")

                self.search_student(student_id)

            elif choice == "4":

                student_id = input("Enter Student ID: ")

                self.update_student(student_id)

            elif choice == "5":

                student_id = input("Enter Student ID: ")

                self.delete_student(student_id)

            elif choice == "6":

                print("\nThank You For Using SMS")
                break

            else:
                print("\nInvalid Choice")

from database.db import Database
from models.faculty import Faculty
from utils.id_generator import generate_id

class FacultyManagementSystem:

    def __init__(self):
        # self.faculties = []
        self.db = Database()

    def register_faculty(self, faculty):

        # self.faculties.append(faculty)

        query = """
            INSERT INTO faculties
            (
                faculty_id,
                name,
                email,
                age,
                mobile,
                specialization,
                gender
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            faculty.faculty_id,
            faculty.name,
            faculty.email,
            faculty.age,
            faculty.mobile,
            faculty.specialization,
            faculty.gender,
        )

        self.db.execute(query, values)

        print("\nFaculty Registered Successfully")

    def view_faculties(self):
        # if len(self.faculties) == 0:
        #     print("\nNo Faculties Found")
        #     return
        #
        # print("\n===== FACULTY LIST =====")
        # for faculty in self.faculties:
        #     faculty.display()

        faculties = self.db.fetch_all("SELECT * FROM faculties")
        if not faculties:
            print("\nNo Faculties Found")
            return

        print("\n===== FACULTY LIST =====")
        for faculty in faculties:
            print("\n----- Faculty Details -----")
            print(f"Faculty ID     : {faculty['faculty_id']}")
            print(f"Name           : {faculty['name']}")
            print(f"Email          : {faculty['email']}")
            print(f"Age            : {faculty['age']}")
            print(f"Mobile         : {faculty['mobile']}")
            print(f"Specialization : {faculty['specialization']}")
            print(f"Gender         : {faculty['gender']}")

    def find_faculty_by_id(self, faculty_id):
        # for faculty in self.faculties:
        #     if faculty.faculty_id == faculty_id:
        #         return faculty
        # return None

        return self.db.fetch_one(
            "SELECT * FROM faculties WHERE faculty_id = %s",
            (faculty_id,)
        )

    def search_faculty(self, faculty_id):
        # faculty = self.find_faculty_by_id(faculty_id)
        # if faculty:
        #     print("\nFaculty Found")
        #     faculty.display()
        #     return
        # else:
        #     print("Faculty Not Found!!")

        faculty = self.find_faculty_by_id(faculty_id)
        if not faculty:
            print("\nFaculty Not Found")
            return

        print("\nFaculty Found")
        print("\n----- Faculty Details -----")
        print(f"Faculty ID     : {faculty['faculty_id']}")
        print(f"Name           : {faculty['name']}")
        print(f"Email          : {faculty['email']}")
        print(f"Age            : {faculty['age']}")
        print(f"Mobile         : {faculty['mobile']}")
        print(f"Specialization : {faculty['specialization']}")
        print(f"Gender         : {faculty['gender']}")

    def update_faculty(self, faculty_id):
        faculty = self.find_faculty_by_id(faculty_id)

        if faculty:
            print("\nLeave blank if you don't want to update.")

            name = input("Enter New Name: ").strip()
            
            while True:
                email = input("Enter New Email: ").strip()
                if not email or ("@" in email and "." in email):
                    break
                print("Invalid email! Please enter a valid email.")

            while True:
                age = input("Enter New Age: ").strip()
                if not age or (age.isdigit() and int(age) > 0):
                    break
                print("Invalid age! Please enter a valid positive number.")

            while True:
                mobile = input("Enter New Mobile: ").strip()
                if not mobile or (mobile.isdigit() and len(mobile) == 10):
                    break
                print("Invalid mobile! Please enter a 10-digit number.")

            specialization = input("Enter New Specialization: ").strip()
            
            while True:
                gender = input("Enter New Gender (male/female/other): ").strip().lower()
                if not gender or gender in ['male', 'female', 'other']:
                    break
                print("Invalid gender! Please enter male, female, or other.")

            # if name:
            #     faculty.name = name
            # if email:
            #     faculty.email = email
            # if age:
            #     faculty.age = age
            # if mobile:
            #     faculty.mobile = mobile
            # if specialization:
            #     faculty.specialization = specialization
            # if gender:
            #     faculty.gender = gender

            name = name if name else faculty['name']
            email = email if email else faculty['email']
            age = age if age else faculty['age']
            mobile = mobile if mobile else faculty['mobile']
            specialization = specialization if specialization else faculty['specialization']
            gender = gender if gender else faculty['gender']

            query = """
            UPDATE faculties
            SET name = %s, email = %s, age = %s, mobile = %s,
                specialization = %s, gender = %s
            WHERE faculty_id = %s
            """
            self.db.execute(
                query,
                (name, email, age, mobile, specialization, gender, faculty_id)
            )

            print("\nFaculty Updated Successfully")

        else:
            print("\nFaculty Not Found")

    def delete_faculty(self, faculty_id):
        # faculty = self.find_faculty_by_id(faculty_id)
        # print("Delete Test : \n", faculty)
        # if faculty:
        #     self.faculties.remove(faculty)
        #     print("Faculty Deleted")
        # else:
        #     print("Faculty Not Found!!")

        if not self.find_faculty_by_id(faculty_id):
            print("\nFaculty Not Found")
            return

        self.db.execute("DELETE FROM faculties WHERE faculty_id = %s", (faculty_id,))
        print("\nFaculty Deleted Successfully")

    def menu(self):
        while True:
            print("\n==============================")
            print(" FACULTY MANAGEMENT SYSTEM ")
            print("==============================")
            print("1. Register Faculty")
            print("2. View Faculties")
            print("3. Search Faculty")
            print("4. Update Faculty")
            print("5. Delete Faculty")
            print("6. Exit")

            choice = input("\nEnter Your Choice: ")

            if choice == "1":

                existing_ids = [
                    faculty['faculty_id']
                    for faculty in self.db.fetch_all("SELECT faculty_id FROM faculties")
                ]
                faculty_id = generate_id("FAC", existing_ids)
                print(f"Generated Faculty ID: {faculty_id}")

                # faculty_id = input("Enter Faculty ID: ")

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
                    age = input("Enter Age: ").strip()
                    if age.isdigit() and int(age) > 0:
                        break
                    print("Invalid age! Please enter a valid positive number.")

                while True:
                    mobile = input("Enter Mobile: ").strip()
                    if mobile.isdigit() and len(mobile) == 10:
                        break
                    print("Invalid mobile! Please enter a 10-digit number.")

                while True:
                    specialization = input("Enter Subject of Specialization: ").strip()
                    if specialization:
                        break
                    print("Specialization cannot be empty!")

                while True:
                    gender = input("Enter Gender (male/female/other): ").strip().lower()
                    if gender in ['male', 'female', 'other']:
                        break
                    print("Invalid gender! Please enter male, female, or other.")

                faculty = Faculty(
                    faculty_id,
                    name,
                    email,
                    age,
                    mobile,
                    specialization,
                    gender
                )

                self.register_faculty(faculty)

            elif choice == "2":
                self.view_faculties()

            elif choice == "3":
                faculty_id = input("Enter Faculty ID: ")
                self.search_faculty(faculty_id)

            elif choice == "4":
                faculty_id = input("Enter Faculty ID: ")
                self.update_faculty(faculty_id)

            elif choice == "5":
                faculty_id = input("Enter Faculty ID: ")
                self.delete_faculty(faculty_id)

            elif choice == "6":
                print("\nThank You For Using FMS")
                break

            else:
                print("\nInvalid Choice")

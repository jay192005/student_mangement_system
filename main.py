from services.student_service import StudentManagementSystem
from services.faculty_service import FacultyManagementSystem
from services.admin_service import AdminManagementSystem

def main():
    sms = StudentManagementSystem()
    fms = FacultyManagementSystem()
    ams = AdminManagementSystem()

    while True:
        print("\n==============================")
        print(" Student Management System ")
        print("==============================")
        print("1. Admin")
        print("2. Faculty")
        print("3. Student")
        print("4. Exit")

        choice = input("\nWho are you? (Enter Choice): ")

        if choice == "1":
            ams.menu()
        elif choice == "2":
            fms.menu()
        elif choice == "3":
            sms.menu()
        elif choice == "4":
            print("\nExiting System. Goodbye!")
            break
        else:
            print("\nInvalid Choice. Please try again.")

main()

from database.db import Database
from models.admin import Admin
from utils.id_generator import generate_id

class AdminManagementSystem:

    def __init__(self):
        # self.admins = []
        self.db = Database()

    def register_admin(self, admin):
        # self.admins.append(admin)

        query = """
        INSERT INTO admins (admin_id, name, email, mobile, gender, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            admin.admin_id,
            admin.name,
            admin.email,
            admin.mobile,
            admin.gender,
            admin.role
        )
        self.db.execute(query, values)
        print("\nAdmin Registered Successfully")

    def view_admins(self):
        # if len(self.admins) == 0:
        #     print("\nNo Admins Found")
        #     return
        #
        # print("\n===== ADMIN LIST =====")
        # for admin in self.admins:
        #     admin.display()

        admins = self.db.fetch_all("SELECT * FROM admins")
        if not admins:
            print("\nNo Admins Found")
            return

        print("\n===== ADMIN LIST =====")
        for admin in admins:
            print("\n----- Admin Details -----")
            print(f"Admin ID : {admin['admin_id']}")
            print(f"Name     : {admin['name']}")
            print(f"Email    : {admin['email']}")
            print(f"Mobile   : {admin['mobile']}")
            print(f"Gender   : {admin['gender']}")
            print(f"Role     : {admin['role']}")

    def find_admin_by_id(self, admin_id):
        # for admin in self.admins:
        #     if admin.admin_id == admin_id:
        #         return admin
        # return None

        return self.db.fetch_one(
            "SELECT * FROM admins WHERE admin_id = %s",
            (admin_id,)
        )

    def search_admin(self, admin_id):
        # admin = self.find_admin_by_id(admin_id)
        # if admin:
        #     print("\nAdmin Found")
        #     admin.display()
        #     return
        # else:
        #     print("Admin Not Found!!")

        admin = self.find_admin_by_id(admin_id)
        if not admin:
            print("\nAdmin Not Found")
            return

        print("\nAdmin Found")
        print("\n----- Admin Details -----")
        print(f"Admin ID : {admin['admin_id']}")
        print(f"Name     : {admin['name']}")
        print(f"Email    : {admin['email']}")
        print(f"Mobile   : {admin['mobile']}")
        print(f"Gender   : {admin['gender']}")
        print(f"Role     : {admin['role']}")

    def update_admin(self, admin_id):
        admin = self.find_admin_by_id(admin_id)

        if admin:
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
            
            while True:
                gender = input("Enter New Gender (male/female/other): ").strip().lower()
                if not gender or gender in ['male', 'female', 'other']:
                    break
                print("Invalid gender! Please enter male, female, or other.")
                
            role = input("Enter New Role: ").strip()

            # if name:
            #     admin.name = name
            # if email:
            #     admin.email = email
            # if mobile:
            #     admin.mobile = mobile
            # if gender:
            #     admin.gender = gender
            # if role:
            #     admin.role = role

            name = name if name else admin['name']
            email = email if email else admin['email']
            mobile = mobile if mobile else admin['mobile']
            gender = gender if gender else admin['gender']
            role = role if role else admin['role']

            query = """
            UPDATE admins
            SET name = %s, email = %s, mobile = %s, gender = %s, role = %s
            WHERE admin_id = %s
            """
            self.db.execute(query, (name, email, mobile, gender, role, admin_id))

            print("\nAdmin Updated Successfully")

        else:
            print("\nAdmin Not Found")

    # Intentionally omitted delete_admin as per requirements

    def delete_admin(self, admin_id):
        if not self.find_admin_by_id(admin_id):
            print("\nAdmin Not Found")
            return

        self.db.execute("DELETE FROM admins WHERE admin_id = %s", (admin_id,))
        print("\nAdmin Deleted Successfully")

    def menu(self):
        while True:
            print("\n==============================")
            print(" ADMIN MANAGEMENT SYSTEM ")
            print("==============================")
            print("1. Register Admin")
            print("2. View Admins")
            print("3. Search Admin")
            print("4. Update Admin")
            print("5. Delete Admin")
            print("6. Exit")

            choice = input("\nEnter Your Choice: ")

            if choice == "1":
                
                # existing_ids = [a.admin_id for a in self.admins]
                # admin_id = generate_id("ADM", existing_ids)
                # print(f"Generated Admin ID: {admin_id}")

                existing_ids = [
                    admin['admin_id']
                    for admin in self.db.fetch_all("SELECT admin_id FROM admins")
                ]
                admin_id = generate_id("ADM", existing_ids)
                print(f"Generated Admin ID: {admin_id}")

                # admin_id = input("Enter Admin ID: ")

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
                    gender = input("Enter Gender (male/female/other): ").strip().lower()
                    if gender in ['male', 'female', 'other']:
                        break
                    print("Invalid gender! Please enter male, female, or other.")
                    
                while True:
                    role = input("Enter Role: ").strip()
                    if role:
                        break
                    print("Role cannot be empty!")

                admin = Admin(
                    admin_id,
                    name,
                    email,
                    mobile,
                    gender,
                    role
                )

                self.register_admin(admin)

            elif choice == "2":
                self.view_admins()

            elif choice == "3":
                admin_id = input("Enter Admin ID: ")
                self.search_admin(admin_id)

            elif choice == "4":
                admin_id = input("Enter Admin ID: ")
                self.update_admin(admin_id)

            elif choice == "5":
                admin_id = input("Enter Admin ID: ")
                self.delete_admin(admin_id)

            elif choice == "6":
                print("\nThank You For Using AMS")
                break

            else:
                print("\nInvalid Choice")

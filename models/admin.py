from auth.permissions import Permission
from models.person import Person

class Admin(Person):

    def __init__(
        self,
        admin_id,
        name,
        email,
        mobile,
        gender,
        role
    ):

        super().__init__(
            name,
            email,
            mobile,
            gender
        )

        self.admin_id = admin_id
        self.role = role

    def display(self):

        print("\n----- Admin Details -----")

        print(f"Admin ID : {self.admin_id}")

        self.display_basic_details()

        print(f"Role     : {self.role}")

    # Method overriding: Admin supplies its own role and permission set.
    def show_role(self):
        return "Admin"

    def show_permissions(self):
        return (
            Permission.VIEW_OWN_PROFILE,
            Permission.VIEW_ACADEMIC_INFORMATION,
            Permission.VIEW_ASSIGNED_STUDENTS,
            Permission.UPDATE_STUDENT_ACADEMIC_INFORMATION,
            Permission.MANAGE_STUDENTS,
            Permission.MANAGE_FACULTY,
            Permission.MANAGE_ADMINS,
            Permission.VIEW_SYSTEM_REPORTS,
        )

    def can_view_academic_information_for(self, student_id):
        return True

    def assigned_student_ids(self):
        # Admin has unrestricted visibility of student records.
        return None

    def can_update_academic_information_for(self, student_id):
        return True

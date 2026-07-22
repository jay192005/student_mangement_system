from auth.permissions import Permission
from models.person import Person

class Student(Person):

    def __init__(
        self,
        student_id,
        name,
        email,
        mobile,
        course,
        gender,
        date_of_birth,
        address
    ):

        # Parent Constructor Call
        super().__init__(
            name,
            email,
            mobile,
            gender
        )

        self.student_id = student_id
        self.course = course
        self.date_of_birth = date_of_birth
        self.address = address

    def display(self):

        print("\n----- Student Details -----")

        print(f"Student ID     : {self.student_id}")

        # Inherited Data
        self.display_basic_details()

        print(f"Course         : {self.course}")
        print(f"Date Of Birth  : {self.date_of_birth}")
        print(f"Address        : {self.address}")

    # Method overriding: Student supplies its own role and permission set.
    def show_role(self):
        return "Student"

    def show_permissions(self):
        return (
            Permission.VIEW_OWN_PROFILE,
            Permission.VIEW_ACADEMIC_INFORMATION,
        )

    def can_view_academic_information_for(self, student_id):
        return self.student_id == student_id

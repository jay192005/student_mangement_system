from auth.permissions import Permission
from models.person import Person

class Faculty(Person):

    def __init__(
        self,
        faculty_id,
        name,
        email,
        age,
        mobile,
        specialization,
        gender,
        assigned_student_ids=None
    ):

        super().__init__(
            name,
            email,
            mobile,
            gender
        )

        self.faculty_id = faculty_id
        self.age = age
        self.specialization = specialization
        # Optional to preserve every existing Phase 1 constructor call. A
        # future assignment table can populate this list after login.
        self._assigned_student_ids = tuple(assigned_student_ids or ())

    def display(self):

        print("\n----- Faculty Details -----")

        print(f"Faculty ID     : {self.faculty_id}")

        self.display_basic_details()

        print(f"Age            : {self.age}")
        print(f"Specialization : {self.specialization}")

    # Method overriding: Faculty supplies its own role and permission set.
    def show_role(self):
        return "Faculty"

    def show_permissions(self):
        return (
            Permission.VIEW_OWN_PROFILE,
            Permission.VIEW_ASSIGNED_STUDENTS,
            Permission.UPDATE_STUDENT_ACADEMIC_INFORMATION,
        )

    def assigned_student_ids(self):
        return self._assigned_student_ids

    def can_update_academic_information_for(self, student_id):
        return student_id in self._assigned_student_ids

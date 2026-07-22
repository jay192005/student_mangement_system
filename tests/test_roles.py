import unittest

from auth.permissions import Permission, PermissionDeniedError, require_permission
from models.admin import Admin
from models.faculty import Faculty
from models.student import Student


class RoleModelTests(unittest.TestCase):
    def setUp(self):
        self.student = Student("STU001", "Student", "s@example.com", "1234567890", "BCA", "other", "2000-01-01", "Pune")
        self.faculty = Faculty("FAC001", "Faculty", "f@example.com", 30, "1234567890", "Python", "other", ["STU001"])
        self.admin = Admin("ADM001", "Admin", "a@example.com", "1234567890", "other", "System Admin")

    def test_overridden_role_methods_are_polymorphic(self):
        users = [self.student, self.faculty, self.admin]
        self.assertEqual([user.show_role() for user in users], ["Student", "Faculty", "Admin"])

    def test_role_specific_permissions(self):
        self.assertTrue(self.student.has_permission(Permission.VIEW_ACADEMIC_INFORMATION))
        self.assertFalse(self.student.has_permission(Permission.MANAGE_STUDENTS))
        self.assertTrue(self.faculty.has_permission(Permission.UPDATE_STUDENT_ACADEMIC_INFORMATION))
        self.assertFalse(self.faculty.has_permission(Permission.MANAGE_ADMINS))
        self.assertTrue(self.admin.has_permission(Permission.MANAGE_ADMINS))

    def test_record_scoping(self):
        self.assertTrue(self.student.can_view_academic_information_for("STU001"))
        self.assertFalse(self.student.can_view_academic_information_for("STU002"))
        self.assertTrue(self.faculty.can_update_academic_information_for("STU001"))
        self.assertFalse(self.faculty.can_update_academic_information_for("STU002"))
        self.assertTrue(self.admin.can_update_academic_information_for("STU002"))

    def test_denied_permission_raises(self):
        with self.assertRaises(PermissionDeniedError):
            require_permission(self.student, Permission.MANAGE_ADMINS)


if __name__ == "__main__":
    unittest.main()

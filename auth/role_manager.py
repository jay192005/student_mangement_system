"""Role-aware application actions.

This class is deliberately independent of login details.  A Phase 3 login
service can pass its authenticated ``Person`` instance as ``user`` without
changing the authorization rules below.
"""

from auth.permissions import Permission, require_permission


class RoleManager:
    """Coordinates permission checks around existing management systems.

    Manager dependencies are injected so existing CRUD classes remain usable
    exactly as they are today and tests can use lightweight substitutes.
    """

    def __init__(self, student_manager=None, faculty_manager=None, admin_manager=None):
        self.student_manager = student_manager
        self.faculty_manager = faculty_manager
        self.admin_manager = admin_manager

    def show_user_access(self, user):
        """Polymorphic role summary for menus, dashboards, or a future login."""
        return {"role": user.show_role(), "permissions": user.show_permissions()}

    def view_own_profile(self, user):
        require_permission(user, Permission.VIEW_OWN_PROFILE)
        return user

    def view_academic_information(self, user, student_id):
        """Allow a student to read only their own record; admins may read any."""
        require_permission(user, Permission.VIEW_ACADEMIC_INFORMATION)
        if not user.can_view_academic_information_for(student_id):
            raise PermissionError("This user cannot view that student's academic information.")
        return self._student_manager().find_student_by_id(student_id)

    def view_assigned_students(self, user):
        require_permission(user, Permission.VIEW_ASSIGNED_STUDENTS)
        assigned_ids = user.assigned_student_ids()
        if assigned_ids is None:
            return self._student_manager().db.fetch_all("SELECT * FROM students")
        return [
            student
            for student_id in assigned_ids
            if (student := self._student_manager().find_student_by_id(student_id))
        ]

    def update_student_academic_information(self, user, student_id, course):
        """Authorize an academic update and delegate it to the CRUD service."""
        require_permission(user, Permission.UPDATE_STUDENT_ACADEMIC_INFORMATION)
        if not user.can_update_academic_information_for(student_id):
            raise PermissionError("This user cannot update that student's academic information.")
        return self._student_manager().update_student_academic_information(student_id, course)

    def student_management(self, user):
        require_permission(user, Permission.MANAGE_STUDENTS)
        return self._student_manager()

    def faculty_management(self, user):
        require_permission(user, Permission.MANAGE_FACULTY)
        return self._faculty_manager()

    def admin_management(self, user):
        require_permission(user, Permission.MANAGE_ADMINS)
        return self._admin_manager()

    def view_system_reports(self, user):
        require_permission(user, Permission.VIEW_SYSTEM_REPORTS)
        return {
            "students": len(self._student_manager().db.fetch_all("SELECT student_id FROM students")),
            "faculty": len(self._faculty_manager().db.fetch_all("SELECT faculty_id FROM faculties")),
            "admins": len(self._admin_manager().db.fetch_all("SELECT admin_id FROM admins")),
        }

    def _student_manager(self):
        if self.student_manager is None:
            raise RuntimeError("A StudentManagementSystem is required for this action.")
        return self.student_manager

    def _faculty_manager(self):
        if self.faculty_manager is None:
            raise RuntimeError("A FacultyManagementSystem is required for this action.")
        return self.faculty_manager

    def _admin_manager(self):
        if self.admin_manager is None:
            raise RuntimeError("An AdminManagementSystem is required for this action.")
        return self.admin_manager

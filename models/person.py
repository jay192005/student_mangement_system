from auth.permissions import Permission


class Person:
    """Base type for every system user.

    Authentication can later attach an authenticated ``Person`` instance to a
    session.  Callers only need this common interface to authorize an action.
    """

    def __init__(self, name, email, mobile, gender):

        self.name = name
        self.email = email
        self.mobile = mobile
        self.gender = gender

    def display_basic_details(self):

        print(f"Name   : {self.name}")
        print(f"Email  : {self.email}")
        print(f"Mobile : {self.mobile}")
        print(f"Gender : {self.gender}")

    def show_role(self):
        """Return the role name. Subclasses provide the concrete role."""
        return "Person"

    def show_permissions(self):
        """Return the permissions granted to this user.

        A tuple is returned so callers cannot accidentally change a role's
        permissions on one object at runtime.
        """
        return ()

    def has_permission(self, permission):
        """Return whether this user has *permission*.

        This is intentionally based on the polymorphic ``show_permissions``
        call rather than on ``isinstance`` or role-name conditionals.
        """
        return permission in self.show_permissions()

    def can_view_academic_information_for(self, student_id):
        """Object-level ownership rule; concrete roles override when needed."""
        return False

    def assigned_student_ids(self):
        """Return assigned IDs, or ``None`` for unrestricted access."""
        return ()

    def can_update_academic_information_for(self, student_id):
        return False

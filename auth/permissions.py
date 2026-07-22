"""Permission vocabulary and authorization helpers for the application."""

from enum import Enum, auto


class Permission(Enum):
    VIEW_OWN_PROFILE = auto()
    VIEW_ACADEMIC_INFORMATION = auto()
    VIEW_ASSIGNED_STUDENTS = auto()
    UPDATE_STUDENT_ACADEMIC_INFORMATION = auto()
    MANAGE_STUDENTS = auto()
    MANAGE_FACULTY = auto()
    MANAGE_ADMINS = auto()
    VIEW_SYSTEM_REPORTS = auto()


class PermissionDeniedError(PermissionError):
    """Raised when a user attempts an action outside their role."""


def require_permission(user, permission):
    """Authorize *user* for *permission* using the common Person contract."""
    if not user.has_permission(permission):
        raise PermissionDeniedError(
            f"{user.show_role()} is not allowed to {permission.name.lower()}."
        )

# Phase 2: Roles and Responsibilities

## Class hierarchy

```text
Person
├── Student
├── Faculty
└── Admin

RoleManager ──uses──> Person
RoleManager ──composes/injects──> StudentManagementSystem
                           ├── FacultyManagementSystem
                           └── AdminManagementSystem
Each management system ──composes──> Database
```

## Role permissions

| Role | Permissions |
| --- | --- |
| Student | View own profile; view own academic information |
| Faculty | View profile; view assigned students; update student academic information |
| Admin | All listed permissions; manage students, faculty, and admins; view reports |

`Person` defines `show_role()`, `show_permissions()`, and `has_permission()`.
`Student`, `Faculty`, and `Admin` override the first two methods.  Therefore a
caller can use `user.show_role()` or `user.show_permissions()` on any `Person`
reference and Python dispatches to the appropriate child implementation. This
is runtime polymorphism; no role-specific `isinstance` chain is needed.

`RoleManager` is the authorization boundary. It calls the common
`user.has_permission()` interface and delegates to the existing CRUD managers.
The per-record ownership/assignment checks are also polymorphic
(`can_view_academic_information_for`, `assigned_student_ids`, and
`can_update_academic_information_for`), avoiding role-type conditionals.
Existing register, view, search, update, and delete methods keep their names
and signatures, so Phase 1 functionality is not replaced.

The existing database stores `course` as the available academic field.
`StudentManagementSystem.update_student_academic_information(student_id, course)`
updates it after `RoleManager.update_student_academic_information(user,
student_id, course)` authorizes the caller. More academic fields can be added
behind this service method in a later phase.

## Future phases

Phase 3 authentication should construct the authenticated `Student`,
`Faculty`, or `Admin` and pass it to `RoleManager`; authorization needs no
rewrite. Phase 4 reports plug into `view_system_reports()`. Phase 5 dashboards
can render `RoleManager.show_user_access(user)` and expose only the returned
permissions.

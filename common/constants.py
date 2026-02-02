class UserRole:
    ADMIN = "ADMIN"
    WARDEN = "WARDEN"
    STUDENT = "STUDENT"

    CHOICES = (
        (ADMIN, "Admin"),
        (WARDEN, "Warden"),
        (STUDENT, "Student"),
    )

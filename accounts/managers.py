from django.contrib.auth.base_user import BaseUserManager
from common.constants import UserRole

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, role=UserRole.STUDENT, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email=email,
            password=password,
            role=UserRole.ADMIN,
            **extra_fields
        )

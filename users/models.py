# import uuid
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.utils.translation import gettext_lazy as _


# class UserRoles:
#     SUPER_ADMIN = "super_admin"
#     ADMIN = "admin"
#     STAFF = "staff"
#     CUSTOMER = "customer"
#     AGENT = "agent"

#     CHOICES = [
#         (SUPER_ADMIN, "Super Admin"),
#         (ADMIN, "Admin"),
#         (STAFF, "Staff"),
#         (CUSTOMER, "Customer"),
#         (AGENT, "Agent"),
#     ]


# class CustomUserManager(BaseUserManager):

#     def create_user(self, contact_number, password=None, **extra_fields):
#         if not contact_number:
#             raise ValueError("Contact number is required")

#         extra_fields.setdefault("is_active", True)
#         extra_fields.setdefault("username", str(uuid.uuid4()))

#         user = self.model(contact_number=contact_number, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, contact_number, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("role", UserRoles.SUPER_ADMIN)

#         return self.create_user(contact_number, password, **extra_fields)


# class CustomUser(AbstractBaseUser, PermissionsMixin):

#     contact_number = models.CharField(_("Phone Number"), max_length=15, unique=True)

#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     email = models.EmailField(blank=True, null=True)
#     first_name = models.CharField(max_length=255, blank=True)
#     last_name = models.CharField(max_length=255, blank=True)

#     role = models.CharField(max_length=20, choices=UserRoles.CHOICES, default=UserRoles.STAFF)
#     biography = models.TextField(blank=True, null=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_deleted = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = "contact_number"
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.contact_number


import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserRoles:
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"
    AGENT = "agent"

    CHOICES = [
        (SUPER_ADMIN, "Super Admin"),
        (ADMIN, "Admin"),
        (STAFF, "Staff"),
        (CUSTOMER, "Customer"),
        (AGENT, "Agent"),
    ]


class CustomUserManager(BaseUserManager):

    def create_user(self, contact_number, password=None, **extra_fields):
        if not contact_number:
            raise ValueError("Contact number is required")

        extra_fields.setdefault("is_active", True)

        user = self.model(contact_number=contact_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contact_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRoles.SUPER_ADMIN)

        return self.create_user(contact_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None  # 🚨 IMPORTANT

    contact_number = models.CharField(_("Phone Number"), max_length=15, unique=True)

    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    role = models.CharField(max_length=20, choices=UserRoles.CHOICES, default=UserRoles.STAFF)
    biography = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "contact_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.contact_number

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
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         if not username:
#             raise ValueError('The Username field must be set')

#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('role', UserRoles.SUPER_ADMIN)

#         if not extra_fields.get('is_staff'):
#             raise ValueError('Superuser must have is_staff=True.')
#         if not extra_fields.get('is_superuser'):
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, username, password, **extra_fields)


# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(_("Email"), unique=True)
#     first_name = models.CharField(_("First Name"), max_length=255)
#     last_name = models.CharField(_("Last Name"), max_length=255)
#     role = models.CharField(max_length=20, choices=UserRoles.CHOICES, default=UserRoles.STAFF)
#     contact_number = models.CharField(max_length=15, blank=True, null=True)
#     biography = models.TextField(blank=True, null=True)

#     is_active = models.BooleanField(_("Is this user active?"), default=True)
#     is_staff = models.BooleanField(_("Is this user staff?"), default=False)
#     is_deleted = models.BooleanField(_("Is this user deleted?"), default=False)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']  # <-- Required so createsuperuser works properly

#     def __str__(self):
#         return self.email

#     def save(self, *args, **kwargs):
#         """ Automatically set is_staff=True for Admins & Super Admins """
#         if self.role in [UserRoles.ADMIN, UserRoles.SUPER_ADMIN]:
#             self.is_staff = True
#         super().save(*args, **kwargs)

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
            raise ValueError("Phone number is required")

        user = self.model(contact_number=contact_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contact_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRoles.SUPER_ADMIN)
        extra_fields.setdefault("is_active", True)

        return self.create_user(contact_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    # 🔥 LOGIN FIELD
    contact_number = models.CharField(
        _("Phone Number"),
        max_length=15,
        unique=True
    )

    # OPTIONAL FIELDS
    email = models.EmailField(_("Email"), blank=True, null=True)
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)

    role = models.CharField(
        max_length=20,
        choices=UserRoles.CHOICES,
        default=UserRoles.STAFF
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "contact_number"
    REQUIRED_FIELDS = []   # 👈 CRITICAL

    def __str__(self):
        return self.contact_number

    def save(self, *args, **kwargs):
        if self.role in [UserRoles.ADMIN, UserRoles.SUPER_ADMIN]:
            self.is_staff = True
        super().save(*args, **kwargs)

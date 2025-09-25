from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from Core.manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    RFID = models.CharField(max_length=50, blank=True, unique=True, null=True)
    Car_Number = models.CharField(max_length=10, blank=True, unique=True, null=True)
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50, blank=True)
    Email = models.EmailField("Email Address", unique=True)
    Phone_Number = models.CharField(max_length=10, unique=True)
    is_card_published = models.BooleanField(default=False)

    is_staff = models.BooleanField(('staff status'), default=False,
                                   help_text=('Designates whether the user can log into this admin '
                                              'site.'))
    is_active = models.BooleanField(('active'), default=True,
                                    help_text=('Designates whether this user should be treated as '
                                               'active. Unselect this instead of deleting accounts.'))
    is_superuser = models.BooleanField(('superuser status'), default=False,
                                       help_text=('Designates that this user has all permissions without '
                                                  'explicitly assigning them.'))

    USERNAME_FIELD = "Email"
    REQUIRED_FIELDS = ["First_Name", "Phone_Number"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.Email}"


class Exit_Point(models.Model):
    class Meta:
        verbose_name = "Exit Point"
        verbose_name_plural = "Exit Points"

    Exit_Point_ID = models.AutoField(primary_key=True)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Enter Valid Email Address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    mobile = models.CharField(max_length=13, unique=True,null=True,blank=True)
    profile_picture=models.ImageField(upload_to="images/profile_pictures/", null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
        if self.pk:  # Only check if the user already exists
            existing = User.objects.filter(pk=self.pk).first()
            if existing and existing.password != self.password:
                self.password = make_password(self.password)  # Hash new password
        else:
            if not self.password.startswith("pbkdf2_sha256$"):  # Only hash if not already hashed
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

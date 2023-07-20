from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError("User should have a username.")

        if email is None:
            raise TypeError("User should have a Email.")

        user = self.model(
            username=username,
            email=self.normalize_email(email=email)
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):

        if password is None:
            raise TypeError("Password should not be a None.")

        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Language(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    id_picture = models.ImageField(upload_to='id_images/', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    languages = models.ManyToManyField(Language)
    fix_pay = models.PositiveIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=20,
                                    help_text="Enter phone number in the format: '+996 555 632-728'")
    home_address = models.TextField(blank=True, null=True)

    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class Courier(User):
    id_courier = models.CharField(max_length=50, unique=True)
    car_brand = models.CharField(max_length=100, blank=True, null=True)
    has_bicycle = models.CharField(max_length=100, blank=True, null=True)
    is_on_foot = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta():
        verbose_name = 'Courier'
        verbose_name_plural = 'Couriers'


class Collectors(User):
    id_collectors = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username

    class Meta():
        verbose_name = 'Collector'
        verbose_name_plural = 'Collectors'


class Blacklist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.customer.username
        


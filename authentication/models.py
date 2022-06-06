from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email,first_name,last_name, phone, password=None ):
        if username is None:
            raise TypeError('Không được bỏ trống username')
        if email is None:
            raise TypeError('Không được bỏ trống Email')
        if first_name is None:
            raise TypeError('Không được bỏ trống first_name')
        if last_name is None:
            raise TypeError('Không được bỏ trống last_name')
        if phone is None:
            raise TypeError('Không được bỏ trống phone')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, last_name='', phone='',first_name=''):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, last_name='', phone='',first_name='')
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    first_name = models.CharField(max_length=250, null=True, blank=True, default='')
    last_name = models.CharField(max_length=250, null=True, blank=True,default='')
    phone = models.CharField(max_length=250, null=True, blank=True, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

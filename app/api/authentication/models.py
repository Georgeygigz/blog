from django.db import models
#from django.contrib.auth.models import User
import jwt
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models
from app.api.models import BaseModel
from datetime import datetime, timedelta
from django.conf import settings
import jwt

class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, *args, **kwargs):
        """Create and return a `User` with an email, username and password."""
        password = kwargs.get('password', '')#the empty quotes means, if pawd not there, pswd will be empty.
        email = kwargs.get('email', '')#the empty quotes means, if pawd not there, default is empty
        del kwargs['email']
        del kwargs['password']
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, *args, **kwargs):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        password = kwargs.get('password', '')
        email = kwargs.get('email', '')
        del kwargs['email']
        del kwargs['password']
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(db_index=True, max_length=255, unique=False)
    last_name = models.CharField(db_index=True, max_length=255, unique=False)
    username = models.CharField(db_index=True, max_length=255, unique=True, default="default-username")
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name',
                       'last_name']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    @classmethod
    def create(self, data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**data)

    @property
    def token(self):
        """This method generates and returns a string of the token generated.
        """
        date = datetime.now() + timedelta(hours=settings.TOKEN_EXP_TIME)

        payload = {
            'email': self.email,
            'exp': int(date.strftime('%s')),
            'id': self.id,
            "username": self.username
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

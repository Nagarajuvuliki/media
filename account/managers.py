from __future__ import unicode_literals

from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserQuerySet(models.QuerySet):

    """ Custom queryset filters for User model """

    def get_by_email(self, email):
        return self.get(email=email)

    def filter_email(self, email):
        return self.filter(email=email)

    def filter_emails(self, emails):
        return self.filter(emails__in=emails)

    def filter_is_active(self, is_active):
        return self.filter(is_active=is_active)

    def filter_contains_albums(self):
        return self.filter(owner_album__isnull=False)



class UserManager(BaseUserManager):

    def create_user(self, email, first_name=None,
                    last_name=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email,
        password and name extra data
        """
        if not email:
            raise ValueError(('Users must have a valid email address'))
        email = self.normalize_email(email).lower()

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name,
                         password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            **extra_fields
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)
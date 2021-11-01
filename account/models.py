from django.db import models
from account.managers import UserQuerySet, UserManager
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin



class User(AbstractBaseUser, PermissionsMixin):
    # user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=30,null=True,blank=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    isdeleted = models.BooleanField(default=False)
    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "role"
    ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @cached_property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_related_client(self):
        has_client = False
        try:
            has_client = (self.user_client is not None)
        except:
            pass
        return has_client

    @property
    def authorization_token(self):
        return self.auth_token.key



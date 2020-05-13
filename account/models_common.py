from django.contrib.auth.models import UserManager
from django.db import models

AUTH_USER_MODEL = 'account.User'


class BaseModelManager(models.Manager):
    pass


class ExtendedUserManager(UserManager):
    pass


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


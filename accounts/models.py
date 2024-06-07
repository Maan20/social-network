from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import *
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
number = RegexValidator(r'^^(\+\d{1,3})?,?\s?\d{9,12}', 'Only numbers are allowed.')

class User(AbstractUser):
    """User model."""
    username        = models.CharField(max_length=128, blank=True, null=True)
    email           = models.EmailField(_('email address'),unique=True)
    full_name       = models.CharField(max_length=100,null=True,blank=True)
    address         = models.CharField(max_length=255, blank=True, null=True)
    gender          = models.PositiveIntegerField(choices=GENDER, default=1)
    is_first_login  = models.BooleanField(default=True)
    status          = models.IntegerField(choices=STATUS_ID,default=ACTIVE_STATE, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)
    updated_at      = models.DateTimeField(auto_now=True, null=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = UserManager()

    def __str__(self):
        return self.email


class FriendRequest(models.Model):
    from_user   = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user     = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    status      = models.PositiveIntegerField(default=PENDING,choices=REQUEST_STATUS)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} > {self.to_user}"
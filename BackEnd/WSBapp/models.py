from django.db import models
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.

class CustomUser(AbstractUser):
    portfolio = models.JSONField(default=list)
    '''
        Light Mode = 0
        Dark Mode = 1
    '''
    theme = models.IntegerField(default=1)
    '''
        Daily = 0
        Weekly = 1
    '''
    newsletter_freq = models.IntegerField(default=1)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    #age = models.IntegerField(default=40)

    #retirement_age = models.IntegerField(default=65)

    '''
        Low = 0
        Medium = 1
        High = 2
    '''

    risk_pref = models.IntegerField(default=0)

    '''
        0 = Not validated
        1 = Validated
    '''
    user_email_validated = models.IntegerField(default=0)
    user_validation_code = models.BigIntegerField(default=random.randint(100000001, 999999998))

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users',
        blank = True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_perms',
        blank = True
    )
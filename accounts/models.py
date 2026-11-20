# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    enrollment_number = models.CharField(
        max_length=20,
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        unique=True
    )

    def __str__(self):
        return self.enrollment_number
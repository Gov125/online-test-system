# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):

    title = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.title


class Question(models.Model):

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )

    question = models.CharField(
        max_length=300
    )

    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)

    correct_answer = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.question


class Result(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )

    score = models.IntegerField()

    total_questions = models.IntegerField()

    percentage = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

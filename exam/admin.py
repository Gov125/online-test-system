from django.contrib import admin

from .models import Exam
from .models import Question
from .models import Result


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'title'
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'question',
        'exam'
    ]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = [
        'student',
        'exam',
        'score',
        'percentage'
    ]

from django.urls import path

from . import views

urlpatterns = [

    path(
        'test/<int:exam_id>/',
        views.start_exam,
        name='test'
    ),

    path(
        'result/',
        views.result_view,
        name='result'
    ),
]
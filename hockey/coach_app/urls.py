from django.urls import path

from . import views

app_name = 'coach'

urlpatterns = [
    path(
        'create_coach_record/<str:team>/<str:season>',
        views.create_coach_record,
        name='create_coach_record'
    ),
]

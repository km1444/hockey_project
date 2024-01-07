from django.urls import path

from . import views

app_name = 'goalkeeper_app'

urlpatterns = [
    path(
        'goalkeeper_stat_alltime/',
        views.goalkeeper_stat_alltime,
        name='goalkeeper_stat'
    ),
]

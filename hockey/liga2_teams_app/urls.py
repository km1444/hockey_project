from django.urls import path

from . import views

app_name = 'liga2_teams'

urlpatterns = [
    path('history/<str:team>/', views.history_team, name='history_team'),
]

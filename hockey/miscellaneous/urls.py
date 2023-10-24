from django.urls import path

from . import views

app_name = 'miscellaneous'

urlpatterns = [
    path('other/filter_start/', views.filter_start, name='filter_start'),
    path(
        'other/filter_view/<str:season_start>/',
        views.filter_view,
        name='filter_view'
    ),
]

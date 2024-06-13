from django.urls import path

from . import views

app_name = 'liga2_seasons'

urlpatterns = [
    path('', views.liga2_index, name='liga2_index'),
    path('<str:season>/', views.liga2_season, name='liga2_season'),
    path('add_team/<str:season>/', views.add_team, name='add_team'),
    path('create_team/<str:season>/', views.create_team, name='create_team'),
    path(
        'add_team_trans_tournament/<str:season>/',
        views.add_team_trans_tournament,
        name='add_team_trans_tournament'),
    path(
        'add_team_addit_tournament/<str:season>/',
        views.add_team_addit_tournament,
        name='add_team_addit_tournament'),
    path(
        'edit_team_in_basic_tournament/<str:season>/<int:pk>/',
        views.edit_team_in_basic_tournament,
        name='edit_team_in_basic_tournament',),
    path(
        'edit_team_in_additional_tournament/<str:season>/<int:pk>/',
        views.edit_team_in_additional_tournament,
        name='edit_team_in_additional_tournament',
    ),
    path(
        'edit_team_in_transition_tournament/<str:season>/<int:pk>/',
        views.edit_team_in_transition_tournament,
        name='edit_team_in_transition_tournament',
    )
]

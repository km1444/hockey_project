from django.urls import path
from goalkeeper_app.views import GoalkeeperStatisticListView

from . import views

app_name = 'goalkeeper_app'

urlpatterns = [
    path(
        'goalkeeper_stat_alltime/',
        views.goalkeeper_stat_alltime,
        name='goalkeeper_stat'
    ),
    path(
        'goalkeeper/<int:pk>/',
        GoalkeeperStatisticListView.as_view(),
        name='goalkeeper_detail'
    ),
]

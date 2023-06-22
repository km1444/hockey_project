# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView, TokenRefreshView, TokenVerifyView,
# )

# from api.views import CommentViewSet, FollowViewSet

# router_v1 = DefaultRouter()
# router_v1.register('posts', PostViewSet)
# router_v1.register('groups', GroupViewSet, basename='group')
# router_v1.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet,
#     basename='comment'
# )
# router_v1.register('follow', FollowViewSet, basename='follows')

# urlpatterns = [
#     path('v1/', include(router_v1.urls)),
#     path('v1/jwt/create/', TokenObtainPairView.as_view()),
#     path('v1/jwt/refresh/', TokenRefreshView.as_view()),
#     path('v1/jwt/verify/', TokenVerifyView.as_view())
# ]
from django.urls import path

from .views import (
    PlayerDetail, PlayerList, PlayerListTeamSeason, SeasonLeadersTeam,
    TeamHistory, TeamList,
)

urlpatterns = [
    path('players/', PlayerList.as_view()),
    path('players/<int:id>/', PlayerDetail.as_view()),
    path('teams/', TeamList.as_view()),
    path('teams/history/<str:team>/', TeamHistory.as_view()),
    path('teams/season_leaders/<str:team>/', SeasonLeadersTeam.as_view()),
    path(
        'team/<str:team>/<str:season>/', PlayerListTeamSeason.as_view()
    ),
]

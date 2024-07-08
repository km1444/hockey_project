from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('rating.urls', namespace='rating')),
    path('', include('miscellaneous.urls', namespace='miscellaneous')),
    path('', include('goalkeeper_app.urls', namespace='goalkeeper_app')),
    path('', include('coach_app.urls', namespace='coach')),
    path(
        'liga2/',
        include('liga2_seasons_app.urls', namespace='liga2_seasons')),
    path(
        'liga2/teams/',
        include('liga2_teams_app.urls', namespace='liga2_teams')),
    path(
        'liga2/players/',
        include('liga2_players_app.urls', namespace='liga2_players')),
    path(
        'liga2/goalkeepers/',
        include('goalkeeper_liga2_app.urls', namespace='goalkeeper_liga2')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
handler404 = 'core.views.page_not_found'
# handler500 = 'core.views.page_not_found'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

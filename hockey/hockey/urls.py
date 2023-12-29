from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('rating.urls', namespace='rating')),
    path('', include('miscellaneous.urls', namespace='miscellaneous')),
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

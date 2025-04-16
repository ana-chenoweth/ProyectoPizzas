from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from social_django.urls import urlpatterns as social_urls
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path("", include(("base.urls", "base"), "base")),
    path('', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL)
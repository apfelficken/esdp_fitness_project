from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


api_url = [
    path('v1/', include('api_v1.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('webapp.urls')),
    path('api/', include(api_url)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

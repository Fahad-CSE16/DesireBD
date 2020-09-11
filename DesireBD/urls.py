
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import homeView
import notifications.urls

urlpatterns = [
    path('', homeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('profile/', include('person.urls')),
    path('tolet/', include('tolet.urls')),
    path('posts/', include('posts.urls')),
    path('rest/', include('rest_api_create.urls')),
    path('api/', include('rest_framework.urls')),
    path('inbox/notifications/',include(notifications.urls, namespace='notifications')),
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

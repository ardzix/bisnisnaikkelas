from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from readiness import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('readiness/', include('readiness.urls', namespace='readiness')),
    # Authentication URLs
    path('accounts/login/', views.login, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
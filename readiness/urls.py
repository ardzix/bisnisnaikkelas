from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='form/', permanent=False), name='readiness'),
    path('form/', views.assessment_form, name='assessment_form'),
    path('submit/', views.submit_assessment, name='submit_assessment'),
    path('processing/<uuid:assessment_id>/', views.processing, name='processing'),
    path('check-status/<uuid:assessment_id>/', views.check_status, name='check_status'),
    path('download/<uuid:assessment_id>/', views.download_report, name='download_report'),
    path('sitemap/', views.sitemap, name='sitemap'),
] 
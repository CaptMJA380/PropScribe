from django.urls import path
from . import views

app_name = 'generator'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('app/', views.app_view, name='app_view'),
    path('upgrade/', views.upgrade_view, name='upgrade_view'),
]

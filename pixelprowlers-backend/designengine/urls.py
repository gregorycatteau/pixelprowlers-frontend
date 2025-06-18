from django.urls import path
from . import views

urlpatterns = [
    path('theme/default/', views.get_default_theme),
    path('theme/<slug:slug>/', views.get_theme_by_slug),
]

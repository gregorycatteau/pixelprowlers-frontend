from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleListView.as_view()),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view()),
    path('categories/', views.CategoryListView.as_view()),
]
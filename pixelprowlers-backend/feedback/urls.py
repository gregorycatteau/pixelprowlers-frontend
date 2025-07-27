# feedback/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet, CommentViewSet

router = DefaultRouter()
# On enregistre d’abord la ViewSet de feedback
router.register(r'feedback', FeedbackViewSet, basename='feedback')
# Puis celle des commentaires, à /api/feedback/comments/
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]

# feedback/views.py
from django.db.models import F
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Feedback, Comment
from .serializers import FeedbackSerializer, CommentSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les notations d’un article (impact, clarté, utilité + commentaire libre)
    """
    queryset = Feedback.objects.select_related('user', 'article').all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # On associe automatiquement l’utilisateur connecté
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD sur les commentaires publics, avec action d’upvote
    """
    queryset = Comment.objects.select_related('user', 'article').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upvote(self, request, pk=None):
        comment = self.get_object()
        # Incrément atomique en base
        Comment.objects.filter(pk=comment.pk).update(upvotes=F('upvotes') + 1)
        comment.refresh_from_db()
        return Response({'upvotes': comment.upvotes})

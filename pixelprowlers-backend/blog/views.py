from rest_framework import generics
from django.utils import timezone
from django.db import models
from django.http import Http404
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer

class ArticleListView(generics.ListAPIView):
    """
    Vue listant tous les articles publiés,
    filtrés en fonction des dates de publication (start_date et end_date).
    """
    serializer_class = ArticleSerializer

    def get_queryset(self):
        now = timezone.now()
        return Article.objects.filter(
            models.Q(start_date__isnull=True) | models.Q(start_date__lte=now),
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now),
            is_published=True
        ).order_by('-created_at')


class ArticleDetailView(generics.RetrieveAPIView):
    """
    Vue détail pour un article précis, récupéré via son slug.
    Vérifie également la publication effective.
    """
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Article.objects.all()

    def get_object(self):
        obj = super().get_object()
        if not obj.is_published:  # <-- correction ici
            raise Http404("Cet article n'est pas publié")
        return obj


class CategoryListView(generics.ListAPIView):
    """
    Vue listant toutes les catégories disponibles.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

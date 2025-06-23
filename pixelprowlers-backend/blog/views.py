from rest_framework import generics
from django.utils import timezone
from django.db import models
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        now = timezone.now()
        return Article.objects.filter(
            models.Q(start_date__isnull=True) | models.Q(start_date__lte=now),
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now),
        ).order_by('-created_at')


class ArticleDetailView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Article.objects.all()


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
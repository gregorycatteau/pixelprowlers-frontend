from rest_framework import serializers
from .models import Category, Article


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'summary',
            'content',
            'category',
            'image',
            'importance',
            'created_at',
            'updated_at',
            'start_date',
            'end_date',
        ]
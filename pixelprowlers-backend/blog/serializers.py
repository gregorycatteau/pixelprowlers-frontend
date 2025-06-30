from rest_framework import serializers
from .models import Category, Article, Author, ArticleSection, Footnote

# Serializer pour la catégorie
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

# Serializer pour les auteurs
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'role', 'avatar']

# Serializer pour les sections d'article
class ArticleSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleSection
        fields = ['title', 'content', 'image', 'order']

# Serializer pour les notes de bas de page
class FootnoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footnote
        fields = ['text', 'order']

# Serializer minimal pour les articles liés (related articles)
class RelatedArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['slug', 'title', 'summary', 'image']

# Serializer principal pour les articles
class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)
    sections = ArticleSectionSerializer(many=True, read_only=True)
    footnotes = FootnoteSerializer(many=True, read_only=True)
    related_articles = RelatedArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'summary',
            'category',
            'image',
            'importance',
            'created_at',
            'updated_at',
            'start_date',
            'end_date',
            'authors',
            'sections',
            'footnotes',
            'related_articles',
        ]

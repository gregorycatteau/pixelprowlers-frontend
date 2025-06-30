from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import datetime

# Catégories
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Auteurs
class Author(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return self.name

# Manager personnalisé pour Article
class ArticleManager(models.Manager):
    def published(self):
        """
        Retourne uniquement les articles publiés maintenant.
        """
        now = timezone.now()
        return self.filter(
            is_published=True,
            start_date__lte=now,
            end_date__gte=now
        )

# Articles
class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    importance = models.CharField(max_length=50, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=datetime.datetime(2099, 12, 31, 23, 59, 0))
    authors = models.ManyToManyField(Author)
    related_articles = models.ManyToManyField("self", blank=True)
    has_introduction = models.BooleanField(default=True)
    has_conclusion = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    objects = ArticleManager()  # ✅ Remplace le manager par celui personnalisé

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def is_published_now(self):
        """
        Vérifie si l'article est actuellement publié.
        """
        now = timezone.now()
        if not self.is_published:
            return False
        if self.start_date and self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True

    def __str__(self):
        return self.title

# Sections d'articles
class ArticleSection(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='article_sections/', blank=True, null=True)
    is_intro = models.BooleanField(default=False)
    is_conclusion = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.article.title} - {self.title or 'Section'}"

# Images multiples pour section
class SectionImage(models.Model):
    section = models.ForeignKey(ArticleSection, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='section_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.section.title or 'Section'} Image"

# Footnotes
class Footnote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='footnotes')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.article.title} - Note {self.order}"

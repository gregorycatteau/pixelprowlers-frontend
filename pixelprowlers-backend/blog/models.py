from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Article(models.Model):
    IMPORTANCE_TOP = 'top'
    IMPORTANCE_MEDIUM = 'medium'
    IMPORTANCE_LOW = 'low'

    IMPORTANCE_CHOICES = [
        (IMPORTANCE_TOP, 'Top'),
        (IMPORTANCE_MEDIUM, 'Medium'),
        (IMPORTANCE_LOW, 'Low'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='articles/')
    importance = models.CharField(max_length=6, choices=IMPORTANCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def is_published(self) -> bool:
        now = timezone.now()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True

    def __str__(self) -> str:
        return self.title
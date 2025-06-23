from django.contrib import admin
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'importance', 'created_at')
    list_filter = ('importance', 'created_at')
    search_fields = ('title', 'category__name')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('created_at', 'updated_at')
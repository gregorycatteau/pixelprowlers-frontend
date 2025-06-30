from django.contrib import admin
from .models import Category, Article, Author, ArticleSection, Footnote, SectionImage

# Admin pour les catégories
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

# Admin pour les auteurs
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')

# Inline pour images supplémentaires
class SectionImageInline(admin.TabularInline):
    model = SectionImage
    extra = 1

# Inline pour sections
class ArticleSectionInline(admin.StackedInline):
    model = ArticleSection
    extra = 0
    show_change_link = True
    ordering = ['order']
    fields = ('title', 'content', 'order', 'image', 'is_intro', 'is_conclusion')
    inlines = [SectionImageInline]

# Inline pour footnotes
class FootnoteInline(admin.StackedInline):
    model = Footnote
    extra = 0

# Admin pour les articles
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'importance', 'is_published', 'created_at', 'has_introduction', 'has_conclusion')
    list_filter = ('importance', 'is_published', 'created_at', 'category')
    search_fields = ('title', 'category__name')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ArticleSectionInline, FootnoteInline]

    fieldsets = (
        ("Informations générales", {
            "fields": ('title', 'slug', 'summary', 'category', 'image', 'importance', 'is_published', 'start_date', 'end_date', 'authors', 'related_articles')
        }),
        ("Options", {
            "fields": ('has_introduction', 'has_conclusion')
        }),
        ("Dates", {
            "fields": ('created_at', 'updated_at')
        }),
    )

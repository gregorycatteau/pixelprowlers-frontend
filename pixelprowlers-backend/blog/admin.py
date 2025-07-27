from django.contrib import admin
from .models import (
    Category, Article, Author, ArticleSection,
    Footnote, SectionImage, ArticleRating
)
from .forms import ArticleSectionAdminForm

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
    form = ArticleSectionAdminForm
    model = ArticleSection
    extra = 0
    show_change_link = True
    ordering = ['order']
    sortable_field_name = 'order'
    fields = ('title', 'content', 'order', 'image', 'is_intro', 'is_conclusion')
    inlines = [SectionImageInline]

# Inline pour footnotes
class FootnoteInline(admin.StackedInline):
    model = Footnote
    extra = 0

# Admin pour les articles
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'importance', 'status', 'visibility',
        'is_featured', 'is_published', 'created_at',
        'has_introduction', 'has_conclusion'
    )
    list_filter = (
        'importance', 'is_published', 'created_at',
        'category', 'status', 'visibility', 'is_featured'
    )
    search_fields = ('title', 'category__name')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ArticleSectionInline, FootnoteInline]

    fieldsets = (
        ("Informations générales", {
            "fields": (
                'title', 'slug', 'summary', 'category', 'image',
                'importance', 'status', 'visibility', 'is_featured',
                'is_published', 'start_date', 'end_date',
                'authors', 'related_articles'
            )
        }),
        ("Options", {
            "fields": ('has_introduction', 'has_conclusion')
        }),
        ("Dates", {
            "fields": ('created_at', 'updated_at')
        }),
    )

# Admin explicite pour les sections
@admin.register(ArticleSection)
class ArticleSectionAdmin(admin.ModelAdmin):
    form = ArticleSectionAdminForm
    list_display = ('article', 'title', 'order', 'is_intro', 'is_conclusion')
    list_filter = ('is_intro', 'is_conclusion', 'article__title')
    search_fields = ('title', 'article__title')
    ordering = ('article', 'order')
    inlines = [SectionImageInline]

# Admin pour les votes utilisateurs
@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = (
        'article', 'criteria_impact',
        'criteria_clarity', 'criteria_utility', 'average_score', 'created_at'
    )
    readonly_fields = (
        'article', 'criteria_impact',
        'criteria_clarity', 'criteria_utility', 'created_at'
    )
    list_filter = ('created_at', 'article__title')
    search_fields = ('article__title',)

    def average_score(self, obj):
        return round(obj.average_score(), 2)

    average_score.short_description = 'Moyenne'

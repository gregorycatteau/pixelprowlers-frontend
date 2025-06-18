from django.contrib import admin
from django.utils.html import format_html
from .models import DesignTheme, UserProfile

@admin.register(DesignTheme)
class DesignThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'primary_color', 'color_preview', 'is_default')
    list_editable = ('is_default',)
    prepopulated_fields = {"slug": ("name",)}

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            obj.primary_color
        )
    color_preview.short_description = "Preview"

    def save_model(self, request, obj, form, change):
        if obj.is_default:
            DesignTheme.objects.exclude(pk=obj.pk).update(is_default=False)
        super().save_model(request, obj, form, change)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'device_type', 'os', 'theme', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('session_id', 'device_type', 'os')

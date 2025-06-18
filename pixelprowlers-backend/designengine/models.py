import django
print("Django version:", django.get_version())

import os
print("DJANGO_SETTINGS_MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE"))

from django.db import models

class DesignTheme(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    primary_color = models.CharField(max_length=7, default="#000000")
    secondary_color = models.CharField(max_length=7, default="#FFFFFF")
    font_family = models.CharField(max_length=100, default="Inter")
    illustration_url = models.URLField(blank=True)
    custom_css = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    session_id = models.CharField(max_length=128, unique=True)
    device_type = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    theme = models.ForeignKey(DesignTheme, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_type} - {self.os} ({self.created_at})"

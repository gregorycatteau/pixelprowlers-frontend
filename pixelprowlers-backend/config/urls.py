# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API des articles / sections, etc.
    path('api/blog/', include('blog.urls')),

    # API du design engine
    path('api/design/', include('designengine.urls')),

    # API feedback (notations + commentaires)
    path('api/feedback/', include('feedback.urls')),
]

# En dev, sert les médias (uploads CKEditor, avatars…)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

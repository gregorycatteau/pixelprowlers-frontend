# feedback/models.py
from django.db import models
from django.conf import settings
from blog.models import Article

class Feedback(models.Model):
    """
    Stocke la notation (impact, clarté, utilité) et
    un commentaire optionnel laissé par un utilisateur
    sur un article donné.
    """
    article    = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    user       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='feedbacks'
    )
    impact     = models.PositiveSmallIntegerField()
    clarity    = models.PositiveSmallIntegerField()
    utility    = models.PositiveSmallIntegerField()
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('article', 'user')
        ordering       = ['-created_at']

    def __str__(self):
        user = self.user.email if self.user else 'Anonyme'
        return f"<Feedback {self.id} by {user} on {self.article.slug}>"

class Comment(models.Model):
    """
    Commentaires publics associés à un article,
    validés par upvotes côté communauté.
    """
    article    = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='comments'
    )
    text       = models.TextField()
    tags       = models.JSONField(default=list)  # ex. ['humour','pertinence']
    upvotes    = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-upvotes', '-created_at']

    def __str__(self):
        return f"<Comment {self.id} on {self.article.slug}>"

# feedback/serializers.py
from rest_framework import serializers
from .models import Feedback, Comment

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            'id', 'article', 'impact', 'clarity',
            'utility', 'comment', 'created_at'
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'user', 'text',
            'tags', 'upvotes', 'created_at'
        ]
        read_only_fields = ['upvotes', 'created_at']

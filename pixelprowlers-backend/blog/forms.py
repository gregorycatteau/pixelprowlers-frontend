from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import ArticleSection

class ArticleSectionAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorWidget(config_name='default'),
        required=False,
        help_text="Contenu enrichi avec mise en forme."
    )

    class Meta:
        model = ArticleSection
        fields = '__all__'

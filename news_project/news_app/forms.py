from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    """
    Form to create or update an Article instance.

    Fields:
        title (str): Title of the article.
        content (str): Main text content of the article.
        publisher (Publisher): The publisher associated with the article.
    """
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']
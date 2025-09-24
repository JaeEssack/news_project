import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Article, Publisher, CustomUser


@pytest.mark.django_db
def test_reader_can_view_approved_articles():
        publisher = Publisher.objects.create(name='Tech News')
        article = Article.objects.create(title='Breaking', content='Content', publisher=publisher, is_approved=True )
user = CustomUser.objects.create_user(username='reader', password='pass', role='reader')


client = APIClient()
client.force_authenticate(user=user)


response = client.get(reverse('article-list'))
assert response.status_code == 200
assert len(response.data) == 1
from rest_framework import serializers
from .models import Article, Publisher


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
            model = Publisher
            fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
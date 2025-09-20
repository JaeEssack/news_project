from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils import timezone


ROLE_CHOICES = [
    ('reader', 'Reader'),
    ('editor', 'Editor'),
    ('journalist', 'Journalist'),
]


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Reader-specific fields
    subscribed_publishers = models.ManyToManyField(
        Publisher, blank=True, related_name='subscribers'
    )
    subscribed_journalists = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='followers'
    )

    # Journalist-specific fields
    bio = models.TextField(blank=True, null=True)
    published_articles = models.ManyToManyField(
        'Article', blank=True, related_name='authors'
    )

    def save(self, *args, **kwargs):
       
        if self.role == 'reader':
            self.bio = None
        elif self.role == 'journalist':
            
            pass

        super().save(*args, **kwargs)

 
        group, created = Group.objects.get_or_create(name=self.role)
        if not self.groups.filter(name=self.role).exists():
            self.groups.add(group)
            

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name='articles'
    )
    journalist = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'role': 'journalist'}
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

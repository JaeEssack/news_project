from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils import timezone


ROLE_CHOICES = [
    ('reader', 'Reader'),
    ('editor', 'Editor'),
    ('journalist', 'Journalist'),
]


class Publisher(models.Model):
    """
    Represents a news publisher.

    Attributes:
        name (str): Name of the publisher.
        description (str): Optional description of the publisher.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Returns the name of the publisher.
        """
        return self.name
    

class CustomUser(AbstractUser):
    """
    Custom user model with roles: reader, editor, or journalist.

    Attributes:
        role (str): The role of the user, must be one of ROLE_CHOICES.
        subscribed_publishers (ManyToMany): Publishers followed by a reader.
        subscribed_journalists (ManyToMany): Journalists followed by a reader.
        bio (str): Optional biography for journalists.
        published_articles (ManyToMany): Articles authored by the journalist.
    """
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
        """
        Overrides the save method to perform additional actions before saving a user.

        Adjusts the user's fields based on their role and adds the user to the corresponding
        Django Group.

        :param args: Additional arguments passed to the parent save method.
        :param kwargs: Additional keyword arguments passed to the parent save method.
        """
        if self.role == 'reader':
            self.bio = None
        elif self.role == 'journalist':
            
            pass

        super().save(*args, **kwargs)

 
        group, created = Group.objects.get_or_create(name=self.role)
        if not self.groups.filter(name=self.role).exists():
            self.groups.add(group)
            

class Article(models.Model):
    """
    Represents a news article.

    Attributes:
        title (str): The title of the article.
        content (str): The main text of the article.
        publisher (ForeignKey): Publisher of the article.
        journalist (ForeignKey): Journalist who wrote the article.
        is_approved (bool): Whether the article has been approved.
        created_at (datetime): When the article was created.
    """
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
        """
        Returns the title of the article.
        """
        return self.title

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Article, CustomUser

@receiver(post_save, sender=Article)
def notify_subscribers_on_approval(sender, instance, created, **kwargs):
    if not created and instance.is_approved:
        subs = set(instance.publisher.subscribers.all())
        if instance.journalist:
            subs.update(instance.journalist.followers.all())

        
        for user in subs:
            send_mail(
                subject=f"New Article: {instance.title}",
                message=instance.content,
                from_email='noreply@newsapp.com',
                recipient_list=[user.email],
                fail_silently=True,
            )


@receiver(post_save, sender=CustomUser)
def clear_irrelevant_m2m(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'reader':
            instance.published_articles.clear()
        elif instance.role == 'journalist':
            instance.subscribed_publishers.clear()
            instance.subscribed_journalists.clear()

            
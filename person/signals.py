from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Person


@receiver(post_save, sender=Person)
def save_profile(sender, instance, **kwargs):
    if instance.is_active != instance.user.is_active:
        instance.user.is_active = instance.is_active
        instance.user.save()

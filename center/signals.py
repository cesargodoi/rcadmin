import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Center


@receiver(post_delete, sender=Center)
def delete_center_image_and_pix_image(sender, instance, **kwargs):
    if instance.image.name != "default_center.jpg":
        os.remove(instance.image.path)
    if instance.pix_image.name != "default_center_pix.jpg":
        os.remove(instance.pix_image.path)

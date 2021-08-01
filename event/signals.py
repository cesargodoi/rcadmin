import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Event
from publicwork.models import Lecture


@receiver(post_save, sender=Event)
def insert_lecture(sender, instance, created, **kwargs):
    if created and instance.activity.activity_type in ("SRV", "CNF"):
        Lecture.objects.create(
            center=instance.center,
            theme=f"{instance.activity.name} (meeting)",
            type="MET",
            date=instance.date,
            description="inserted along with the service",
            made_by=instance.made_by,
        )


@receiver(post_delete, sender=Event)
def delete_event_qr_code_image(sender, instance, **kwargs):
    os.remove(instance.qr_code.path)

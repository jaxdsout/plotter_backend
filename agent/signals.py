from django.db.models.signals import post_save
from djoser.signals import user_activated
from django.dispatch import receiver
from user.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(user_activated)
def create_profile_on_activation(sender, user, request, **kwargs):
    Profile.objects.get_or_create(user=user)


from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        p_name = ''
        if instance.first_name:
            p_name = instance.first_name
        if instance.last_name:
            p_name += instance.last_name
            if not p_name:
                p_name = 'Annonymous'
        Profile.objects.create(user=instance, profile_name=p_name)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import CarImage, SiteSettings


def _delete_file(field_file):
    """Remove a FieldFile from its storage, if it actually points to a file."""
    if not field_file or not field_file.name:
        return
    storage = field_file.storage
    try:
        if storage.exists(field_file.name):
            storage.delete(field_file.name)
    except Exception:
        # Never let a storage/file error break a DB delete/save.
        pass


# ---------- CarImage: photo attached to a car listing ----------

@receiver(post_delete, sender=CarImage)
def delete_car_image_file_on_delete(sender, instance, **kwargs):
    """
    Fired when a CarImage row is deleted - either directly (removing one
    photo) or via CASCADE when the parent CarListing is deleted. Django's
    delete collector sends this signal for every cascaded row too, so
    deleting a whole listing cleans up all of its photos automatically.
    """
    _delete_file(instance.image)


@receiver(pre_save, sender=CarImage)
def delete_old_car_image_file_on_change(sender, instance, **kwargs):
    """
    Fired before a CarImage row is saved. If it already exists in the DB
    and its `image` file is being replaced with a different one, remove
    the old file so it doesn't linger on disk.
    """
    if not instance.pk:
        return
    try:
        old = CarImage.objects.get(pk=instance.pk)
    except CarImage.DoesNotExist:
        return

    old_file = old.image
    new_file = instance.image
    if old_file and old_file.name != getattr(new_file, "name", None):
        _delete_file(old_file)


# ---------- SiteSettings: same problem can happen with the avatar ----------

@receiver(pre_save, sender=SiteSettings)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = SiteSettings.objects.get(pk=instance.pk)
    except SiteSettings.DoesNotExist:
        return

    old_file = old.avatar
    new_file = instance.avatar
    if old_file and old_file.name != getattr(new_file, "name", None):
        _delete_file(old_file)

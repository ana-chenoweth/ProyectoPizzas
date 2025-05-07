from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps  # 👈 necesario para evitar el import circular

class workmateUser(AbstractUser):
    Roles = {
        ("Developer", "Desarollador"),
        ("Project Manager", "Project Manager"),
        ("Other", "Otro/No listado")
    }

    email = models.EmailField(unique=True)
    description = models.CharField(max_length=20, choices=Roles)

    def __str__(self):
        return self.username

@receiver(post_save, sender=workmateUser)
def assign_permissions(sender, instance, created, **kwargs):
    if created and instance.description == "Other":
        InventoryItem = apps.get_model('tasks', 'InventoryItem')  # 👈 OK
        content_type = ContentType.objects.get_for_model(InventoryItem)
        permission = Permission.objects.get(
            codename='add_inventoryitem',
            content_type=content_type
        )
        instance.user_permissions.add(permission)

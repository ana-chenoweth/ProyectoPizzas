from django.contrib.auth.models import AbstractUser
from django.db import models

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

# Create your models here.

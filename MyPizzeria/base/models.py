from django.db import models


# Create your models here.
class Button(models.Model):
    title = models.CharField(max_length=100)
    admin_button = models.BooleanField(default=False)
    base_button = models.BooleanField(default=False)
    link = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

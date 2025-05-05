from django.db import models
from django import forms
from django.forms import ModelChoiceField
from workmates.models import workmateUser

class InventoryItem(models.Model):
    
    Item_types = {
        ("CHEESE", "Cheese"),
        ("MEAT", "Meat"),
        ("VEGETABLE", "Vegetable"),
        ("OTHER", "Other")
    }
    
    name = models.CharField(max_length = 100, blank=False)
    description = models.TextField(max_length = 600, blank=True)
    quantity = models.PositiveBigIntegerField(default=0)
    expiry_date = models.DateField()
    item_type = models.CharField(max_length = 20,choices=Item_types)
    added_by = models.ForeignKey(workmateUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name, self.description, self.item_type, self.quanity, self.expiry_date, self.user.first_name
'''
    @classmethod
    def count_by_progress(cls, progress_status):
        return cls.objects.filter(progress=progress_status).count()
'''
class TaskProfile(models.Model):
    user = models.ForeignKey(workmateUser, on_delete=models.CASCADE)
    task = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.task.description}"

# Create your models here.

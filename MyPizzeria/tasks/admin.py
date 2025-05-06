from django.contrib import admin
from .models import InventoryItem
from .models import TaskProfile

# Register your models here.
admin.site.register(InventoryItem)
admin.site.register(TaskProfile)
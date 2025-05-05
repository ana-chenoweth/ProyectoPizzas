from django.contrib import admin
from .models import Tasks
from .models import TaskProfile

# Register your models here.
admin.site.register(Tasks)
admin.site.register(TaskProfile)
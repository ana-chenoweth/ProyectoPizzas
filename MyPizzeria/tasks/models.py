from django.db import models
from django import forms
from django.forms import ModelChoiceField
from workmates.models import workmateUser

class Tasks(models.Model):
    class Urgency (models.IntegerChoices):
        LV1 = 1, "Level 1"
        LV2 = 2, "Level 2"
        LV3 = 3, "Level 3"
        LV4 = 4, "Level 4"
        LV5 = 5, "Level 5"

    class Completion (models.IntegerChoices):
        Completed = 1, "Completed"
        Incomplete = 2, "Incomplete"
        NotStarted = 3, "Not started"

    Categories = {
        ("TECH", "Technological"),
        ("ADMIN", "Administrative"),
        ("DEV", "Development"),
        ("TEAM", "WorkMate Internal"),
        ("OTHER", "Other")
    }
    
    title = models.TextField(max_length = 300, blank=False)
    description = models.TextField(max_length = 600, blank=False)
    datelimit = models.DateTimeField()
    category = models.CharField(max_length = 20,choices=Categories)
    priority = models.IntegerField(default=Urgency.LV1, choices=Urgency, blank=False)
    notes = models.TextField(max_length = 300, blank=True)
    user = models.ForeignKey(workmateUser, on_delete=models.CASCADE)
    progress = models.IntegerField(default=Completion.NotStarted, choices=Completion, blank=False)

    def __str__(self):
        return self.title, self.description, self.category, self.priority, self.notes, self.user.first_name, self.user.last_name, self.progress

    @classmethod
    def count_by_progress(cls, progress_status):
        return cls.objects.filter(progress=progress_status).count()

class TaskProfile(models.Model):
    user = models.ForeignKey(workmateUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.task.description}"

# Create your models here.

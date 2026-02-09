from django.db import models
from django.contrib.auth.models  import User

class Task(models.Model):
    class STATUS(models.TextChoices):
        NOT_STARTED = 'Not Started', 'Not Started'
        IN_PROGRESS = 'In Progress', 'In Progress'
        COMPLETED = 'Completed', 'Completed'

    title = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.NOT_STARTED)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


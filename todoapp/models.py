from django.db import models


class ToDoTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

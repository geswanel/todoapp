from django.db import models
from django.contrib.auth.models import User


class ToDoTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=True, db_index=True)

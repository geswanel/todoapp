from django import forms

from . import models


class ToDoTaskForm(forms.ModelForm):
    class Meta:
        model = models.ToDoTask
        fields = ['title', 'description']

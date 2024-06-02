from django.shortcuts import render

from .models import ToDoTask


def index(request):
    tasks = ToDoTask.objects.all()
    return render(request, 'todoapp/index.html', {'tasks': tasks})

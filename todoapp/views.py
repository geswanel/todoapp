from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize

import json

from .models import ToDoTask


def index(request):
    if request.method == 'GET':
        tasks = ToDoTask.objects.all()
        return render(request, 'todoapp/index.html', {'tasks': tasks})
    elif request.method == 'POST':
        return create_task(request)


def create_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('task_title', None)
            description = data.get('task_description', None)
            if title is None or description is None:
                return JsonResponse(
                    {'success': False, 'error': 'Wrong payload'},
                    status=400
                )
            else:
                task = ToDoTask.objects.create(
                    title=title,
                    description=description
                )
                return JsonResponse(
                    {'success': True, 'task': serialize('json', [task])},
                    status=201
                )
        except json.JSONDecodeError:
            return JsonResponse(
                {'success': False, 'error': 'Invalid JSON'},
                status=400
            )
    return JsonResponse(
        {'success': False, 'error': 'Invalid method'},
        status=405
    )

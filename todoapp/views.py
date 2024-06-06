from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.forms.models import model_to_dict

import json

from .models import ToDoTask


@login_required     # LOGIN_URL
def index(request):
    if request.method == 'GET':
        today_tasks = ToDoTask.objects.filter(
            date=datetime.now().date(),
            user=request.user,
        )
        yesterday_tasks = ToDoTask.objects.filter(
            date=(datetime.now() - timedelta(days=1)).date(),
            user=request.user,
        )
        context = {
            "tasks_by_day": [
                {"tasks": today_tasks, "day": "today"},
                {"tasks": yesterday_tasks, "day": "yesterday"},
            ]
        }
        return render(request, 'todoapp/index.html', context)
    elif request.method == 'POST':
        return create_task(request)
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        return delete_task(request, data.get('task_id', None))


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
                    description=description,
                    user=request.user,
                )
                return JsonResponse(
                    {'success': True, 'task': model_to_dict(task)},
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


def delete_task(request, id):
    if id:
        try:
            task = ToDoTask.objects.get(pk=id, user=request.user)
            task.delete()
            return JsonResponse(
                {'success': True, 'message': 'task is deleted'},
                status=200
            )
        except ToDoTask.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not Found'},
                                status=404)

    return JsonResponse({'success': False, 'error': 'No id was given.'},
                        status=400)

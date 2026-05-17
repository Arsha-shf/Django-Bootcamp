from django.shortcuts import render
from .models import Task
from django.contrib.auth.decorators import login_required

@login_required
def task_list(request):
    user_tasks = Task.objects.filter(user=request.user)
    context = {
        "tasks": user_tasks
    }

    return render(request, "todos/task_list.html", context)
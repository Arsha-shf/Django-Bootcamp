from django.shortcuts import render, redirect, get_object_or_404
from todos.forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required


@login_required
def task_list(request):
    user_tasks = Task.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "tasks": user_tasks
    }

    return render(request, "todos/task_list.html", context)

@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task-list")
    else:
        form = TaskForm()
    return render(request, "todos/create_task.html", {"form": form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task-list")
    else:
        form = TaskForm(instance=task)
    return render(request, "todos/edit_task.html", {"form": form, "task": task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task-list")
    return render(request, "todos/delete_task.html", {"task": task})

@login_required
def toggle_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.is_done = not task.is_done
        task.save()
    return redirect('task-list')

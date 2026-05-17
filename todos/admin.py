from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "is_done", "created_at", "updated_at", "user")
    list_filter = ("is_done", "created_at", "updated_at")
    search_fields = ("title", "description")

admin.site.register(Task, TaskAdmin)

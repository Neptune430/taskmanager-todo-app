from django.contrib import admin
from taskmanager.models import Task

admin.site.register(Task)  # Registering the Task model with the admin site
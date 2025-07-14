from django.db import models # This is a Django model file for the task manager application.
from django.contrib.auth.models import User # Importing the User model to associate tasks with users.


class Task(models.Model):
    srno=models.AutoField(primary_key=True,auto_created=True)  # Auto-incrementing primary key
    title = models.CharField(max_length=100)  # Title of the task
    date = models.DateTimeField(auto_now_add=True)  # Date associated with the task
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to the User model
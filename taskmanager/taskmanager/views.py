from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages  # Import messages for feedback
from django.utils.translation import gettext as _  # For translation support
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required  # Import for login required
from . import models

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')

        # Basic validation
        if not fnm or not email or not pwd:
            messages.error(request, _("All fields are required."))
            return render(request, 'signup.html')

        # Check if the username (fnm) or email already exists
        if User.objects.filter(username=fnm).exists():
            messages.error(request, _("Username already exists. Please choose another."))
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, _("Email is already in use. Please use another."))
            return render(request, 'signup.html')

        try:
            # Create the user
            my_user = User.objects.create_user(username=fnm, email=email, password=pwd)
            my_user.save()
            messages.success(request, _("Account created successfully! Please log in."))
            return redirect('/login')
        except Exception as e:
            messages.error(request, _("An error occurred: ") + str(e))

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            auth_login(request, userr)
            return redirect('/todopage')
        else:
            messages.error(request, _("Invalid username or password."))
            return redirect('/login')
    return render(request, 'login.html')  # Render the login view


@login_required(login_url='/login')  # Ensure the user is logged in to access this view
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.Task(title=title, user=request.user)
        obj.save()
        # Redirect to the todopage after saving the task
        return redirect('/todopage')  # No need to pass context here

    # If the request method is GET, render the todo page
    res = models.Task.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})  # Pass the tasks to the template


@login_required(login_url='/login')   # Ensure the user is logged in to access this view
def edit_todo(request, srno):
    try:
        obj = models.Task.objects.get(srno=srno, user=request.user)  # Ensure the task belongs to the user
    except models.Task.DoesNotExist:
        messages.error(request, _("Task not found."))
        return redirect('/todopage')

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:  # Check if title is provided
            obj.title = title  # Update the title of the task
            obj.save()
            messages.success(request, _("Task updated successfully!"))
            return redirect('/todopage')  # Redirect after saving the task
        else:
            messages.error(request, _("Title cannot be empty."))

    # If the request method is GET, render the edit form
    return render(request, 'edit_todo.html', {'task': obj})  # Pass the task to the template

@login_required(login_url='/login')
def delete_todo(request, srno):
    obj=models.Task.objects.get(srno=srno, user=request.user)  # Ensure the task belongs to the user
    obj.delete()  # Delete the task
    messages.success(request, _("Task deleted successfully!"))
    return redirect('/todopage')  # Redirect to the todo page after deletion


def signout(request):
    logout(request)  # Log out the user
    messages.success(request, _("You have been logged out successfully."))
    return redirect('/login')  # Redirect to the login page after signing out

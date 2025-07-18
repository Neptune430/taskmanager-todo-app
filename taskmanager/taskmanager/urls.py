from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),  # Optionally name this route
    path('login/', views.login, name='login'),  # Assuming you have a login view
    path('todopage/', views.todo, name='todo'),  # Add name='todo' here 
    path('edit_todo/<int:srno>', views.edit_todo, name='edit_todo'),  # Add name='edit_todo' here
    path('delete_todo/<int:srno>', views.delete_todo, name='delete_todo'),  # Add name='delete_todo' here
    path('signout/', views.signout, name='signout'),  # Add signout view
]

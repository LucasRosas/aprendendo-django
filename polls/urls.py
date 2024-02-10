from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('tasks', views.tasks),
    path('tasks/<int:pk>', views.task_detail),
]
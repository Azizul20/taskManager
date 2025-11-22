
from django.urls import path
from .views import (
    register_view, login_view, logout_view,
    task_list, task_create, task_update, task_delete,task_detail
)

urlpatterns = [
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),

    path('', task_list, name="task_list"),
    path('create/', task_create, name="task_create"),
    path('update/<int:pk>/', task_update, name="task_update"),
    path('delete/<int:pk>/', task_delete, name="task_delete"),
    path('detail/<int:pk>/', task_detail, name="task_detail"),

]

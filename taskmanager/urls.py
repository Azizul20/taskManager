from django.contrib import admin
from django.urls import path, include
from tasks import urls
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", lambda request: redirect("task_list"), name="home"),

    path('admin/', admin.site.urls),
    
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('tasks/', include(urls)),
]

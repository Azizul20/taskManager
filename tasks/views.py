from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from django.utils.timezone import now, timedelta
from django.db.models import Q
from django.http import HttpResponseForbidden


# REGISTER
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "tasks/signup.html", {"form": form})


# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("task_list")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "tasks/login.html")


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")


# CREATE TASK
@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})


# LIST + SEARCH + FILTER + SORT
@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)

    # 1. SEARCH
    search = request.GET.get("search")
    
    
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
          
        )
        
    

    # 2. FILTER STATUS
    status = request.GET.get("status")
    
    print(status)
    if status:
        # status=status.lower()
        tasks = tasks.filter(status=status)

    # 3. FILTER PRIORITY
    priority = request.GET.get("priority")
    print("priority",priority)
    if priority:
        # priority=priority.lower()
        tasks = tasks.filter(priority=priority)

    # 4. FILTER DUE DATE
    due = request.GET.get("due")
    today = now().date()
    week_end = today + timedelta(days=7)

    if due == "today":
        tasks = tasks.filter(due_date=today)
    elif due == "week":
        tasks = tasks.filter(due_date__range=[today, week_end])
    elif due == "overdue":
        tasks = tasks.filter(due_date__lt=today)

    # 5. SORT
    sort = request.GET.get("sort")
    if sort == "oldest":
        tasks = tasks.order_by("created_at")
    else:
        tasks = tasks.order_by("-created_at")

    return render(request, "tasks/task_list.html", {"tasks": tasks})


# UPDATE TASK
@login_required
def task_update(request, pk):
    task = Task.objects.get(id=pk)

    if task.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {"form": form})


# DELETE TASK
@login_required
def task_delete(request, pk):
    task = Task.objects.get(id=pk)

    if task.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/task_confirm_delete.html", {"task": task})


# DETAIL VIEW
@login_required
def task_detail(request, pk):
    task = Task.objects.get(id=pk)

    if task.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    return render(request, "tasks/task_detail.html", {"task": task})

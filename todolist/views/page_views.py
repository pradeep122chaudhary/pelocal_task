from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login-page/")
def HomeView(request):
    """
    Protected dashboard page
    """
    return render(request, "todo/task_list.html")


def LoginView(request):
    """
    Login page (UI only)
    """
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "todo/login.html")


def RegisterView(request):
    """
    Register page (UI only)
    """
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "todo/register.html")

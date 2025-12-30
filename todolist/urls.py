from django.urls import path
from .views.page_views import HomeView, LoginView, RegisterView
from .views.auth_api_views import RegisterAPIView, LoginAPIView, LogoutAPIView
from .views.task_api_views import TaskListCreateAPIView, TaskDetailAPIView
urlpatterns = [

    # UI pages
    path("", HomeView, name="home"),
    path("login-page/", LoginView, name="login-page"),
    path("register-page/", RegisterView, name="register-page"),

    # Task APIs
    path("tasks/", TaskListCreateAPIView.as_view()),
    path("tasks/<int:pk>/", TaskDetailAPIView.as_view()),

    # Auth APIs
    path("auth/register/", RegisterAPIView.as_view()),
    path("auth/login/", LoginAPIView.as_view()),
    path("auth/logout/", LogoutAPIView.as_view()),
]

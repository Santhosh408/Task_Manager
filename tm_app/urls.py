from django.urls import path
from .views import RegisterApiView,LoginApiView,LogoutApiView,TaskApiView,TaskDetailApiView,TaskPriorityApiView

urlpatterns = [
    path('register/',RegisterApiView.as_view()),
    path('login/',LoginApiView.as_view()),
    path('logout/',LogoutApiView.as_view()),
    path('task/',TaskApiView.as_view()),
    path('task/<int:pk>/',TaskDetailApiView.as_view()),
    path('task/<str:pri>/',TaskPriorityApiView.as_view()),
]
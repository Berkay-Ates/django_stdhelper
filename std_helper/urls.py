"""std_helper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import (
    users,
    lessons,
    create_user,
    login_user,
    activate_account,
    create_lesson,
    delete_lesson,
    set_meal_notify,
    user_lessons,
    do_scheduled_jobs
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", users),
    path("lessons/", lessons),
    path("createuser/", create_user),
    path("loginuser/", login_user),
    path("activateaccount/<str:mail>/", activate_account),
    path("createlesson/", create_lesson),
    path("deletelesson/<str:lesson>/", delete_lesson),
    path("setmealnotify/", set_meal_notify),
    path("userlessons/<str:user>/", user_lessons),
    path("scheduledjobs/",do_scheduled_jobs)
]

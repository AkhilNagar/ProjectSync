"""
URL configuration for projectsync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from mainapp import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/",views.user_login, name="login"),
    path("logout/",views.user_logout, name="logout"),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('explore/', views.explore, name="explore"),
    path('projectDetails/<int:pk>/',views.projectDetails, name="projectDetails"),
    path('uploadProjects/',views.uploadProjects, name="uploadProjects"),
    path('univhome/', views.univhome, name="univhome"),
    path('studentprofile/',views.studentprofile,name="studentprofile"),
    path('follow/<int:pk>/', views.follow, name="follow"),    
    path('feed/',views.feed,name="feed"),
    path('updates/<int:pk>/',views.updates, name="updates"),
]

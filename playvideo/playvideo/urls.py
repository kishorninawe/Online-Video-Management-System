"""playvideo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.UserLoginView.as_view(), name='index'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.SignUpView.as_view(), name='register'),

    path('home/', views.ShowHomePage.as_view(), name='home'),
    path('upload_video/', views.UploadVideo.as_view(), name='upload_video'),
    path('my_videos/', views.MyVideos.as_view(), name='my_videos'),
    path('edit_video_details/', views.EditVideoDetails.as_view(), name='edit_video_details'),
    path('delete_video/', views.DeleteVideo.as_view(), name='delete_video'),
    path('account/', views.MyAccount.as_view(), name='account'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('disclaimer/', TemplateView.as_view(template_name='disclaimer.html'), name='disclaimer')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


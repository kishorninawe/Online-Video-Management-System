from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView)
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, UpdateView, DeleteView)
from django_filters.views import FilterView

from app.admin import UserCreationForm
from app.filters import CategoryFilter
from app.forms import VideoDetailForm
from app.models import UserModel, VideoDetailModel


class UserLoginView(LoginView):
    template_name = 'registration/login.html'


class UserLogoutView(LogoutView):
    next_page = '/login/'


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class ShowUser(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    template_name = 'home.html'
    model = UserModel

    def get_object(self, **kwargs):
        return get_object_or_404(UserModel, pk=self.request.user.user_id)


class ShowHomePage(LoginRequiredMixin, FilterView, Paginator):
    filterset_class = CategoryFilter
    login_url = '/login/'
    template_name = 'home.html'
    model = VideoDetailModel
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(ShowHomePage, self).get_context_data(**kwargs)
        context['user_full_name'] = self.request.user.full_name
        context['user_email'] = self.request.user.email
        return context

    def get_queryset(self):
        queryset = super(ShowHomePage, self).get_queryset()
        queryset = queryset.select_related('user_id', 'categories').order_by('date_uploaded')
        return queryset


class UploadVideo(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = VideoDetailForm
    template_name = "upload_video.html"
    success_url = '/home/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(UploadVideo, self).form_valid(form)


class MyVideos(LoginRequiredMixin, FilterView, Paginator):
    filterset_class = CategoryFilter
    login_url = '/login/'
    template_name = 'my_videos.html'
    model = VideoDetailModel
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(MyVideos, self).get_context_data(**kwargs)
        context['user_full_name'] = self.request.user.full_name
        context['user_email'] = self.request.user.email
        return context

    def get_queryset(self):
        queryset = super(MyVideos, self).get_queryset()
        queryset = queryset.filter(user_id_id=self.request.user.user_id).order_by('date_uploaded')
        return queryset


class MyAccount(LoginRequiredMixin, UpdateView):
    template_name = 'account.html'
    model = UserModel
    fields = ('full_name', 'email')
    success_url = reverse_lazy('account')

    def get_object(self, **kwargs):
        return get_object_or_404(UserModel, pk=self.request.user.user_id)


class DeleteVideo(LoginRequiredMixin, DeleteView):
    template_name = 'delete_video.html'
    form_class = VideoDetailForm
    success_url = '/my_videos/'

    def get_object(self, **kwargs):
        return VideoDetailModel.objects.get(pk=self.request.GET.get('video_id'))


class EditVideoDetails(LoginRequiredMixin, UpdateView):
    template_name = 'edit_video_details.html'
    form_class = VideoDetailForm

    def get_success_url(self):
        success_url = '/edit_video_details/?video_id=' + self.request.GET.get('video_id')
        return success_url

    def get_object(self, **kwargs):
        return VideoDetailModel.objects.get(pk=self.request.GET.get('video_id'))

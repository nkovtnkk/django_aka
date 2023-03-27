from django.shortcuts import render, redirect
from django.views.generic import View
from users.models import *

from .forms import *
from .models import *
from .service import *


class HomePage(View):
    def get(self, request, *args, **kwargs):
        users = check_user_and_rangom_user(request.user.id)
        if not users:
            return render(request, 'photos/main.html')
        random_user = users[1]
        time_expired = random_user.time_expired
        random_user = CustomUser.objects.get(pk=random_user.random_user_id)
        context = {
            'random_user': random_user,
            'time_expired': time_expired + datetime.timedelta(hours=1),
            'button_disabled': is_button_disabled(time_expired, 1)
        }
        return render(request, 'photos/main.html', context)

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=request.user.pk)
        random_user = update_or_create_random_user_model(user, get_random_user())
        context = {
            'random_user': random_user.random_user,
            'time_expired': random_user.time_expired + datetime.timedelta(hours=1),
            'button_disabled': True
        }
        return render(request, 'photos/main.html', context)


class CRUDFolder(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        if method == 'patch':
            return self.patch(*args, **kwargs)
        return super(CRUDFolder, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        user = CustomUser.objects.filter(pk=request.POST.get('user_id'))[0]
        Folder.objects.create(name=name, user=user)
        return redirect('users:profile', user_pk=user.pk)

    def delete(self, request):
        user = CustomUser.objects.filter(pk=request.POST['user_id'])[0]
        folder_id = request.POST['folder_id']
        Folder.objects.filter(pk=folder_id).delete()
        return redirect('users:profile', user_pk=user.pk)

    def patch(self, request):
        user = CustomUser.objects.filter(pk=request.POST['user_id'])[0]
        request_dict = request.POST
        Folder.objects.filter(pk=request_dict['folder_id']).update(name=request_dict['name'])
        return redirect('users:profile', user_pk=user.pk)


def create_post(request):
    user_id = request.POST['user']
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    return redirect('users:profile', user_pk=user_id)


def delete_post(request):
    user = CustomUser.objects.filter(pk=request.POST['user_id'])[0]
    Post.objects.filter(pk=request.POST['post_id']).delete()
    return redirect('users:profile', user_pk=user.pk)


def update_post(request):
    user = CustomUser.objects.filter(pk=request.POST['user'])[0]
    request_dict = request.POST
    Post.objects.filter(pk=request_dict['post_id']).update(text=request_dict['text'],
                                                           folder=request_dict['folder'])
    return redirect('users:profile', user_pk=user.pk)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.db.models import Q
from django.views.generic.edit import FormView, View
from .models import *
from .forms import *
from photos.forms import *
from photos.models import *


class UserProfileView(View):

    def get(self, request, user_pk, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=user_pk)
        folders = Folder.objects.filter(user_id=user.pk)
        photos = Post.objects.filter(user_id=user.pk)


        context = {
            'current_user': user,
            'folders': folders,
            'photos': photos,
        }

        return render(request, 'users/profile.html', context=context)



class SearchUsersView(View):


    def get(self, request, *args, **kwargs):
        search_name = request.GET.get("search_name")
        if search_name:
            users = CustomUser.objects.filter(Q(username__icontains=search_name)|
                                   Q(inst_name__icontains=search_name))
            context = {
                'users': users
            }
            return render(request, 'users/users_search.html', context)
        return render(request, 'users/users_search.html', {})



class RegisterFormView(FormView):

    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            form.save()
            user_data = form.cleaned_data
            user = authenticate(
                request, username=user_data.get('username'), password=user_data.get('password1')
            )
            login(request, user)
            return self.form_valid(form)
        else:
            messages.success(request, ('There Was An Error Register, Try Again...'))
            return self.form_invalid(form)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:profile', user_pk=user.pk)
        else:
            messages.success(request, ('There Was An Error Loggin In, Try Again...'))
            return redirect('users:login',)
    else:
        return render(request, 'auth/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('photos:home_page')


def update_user_params(request):
    request_dict = request.POST
    user = CustomUser.objects.filter(pk=request_dict['user_id'])
    user.update(username=request_dict['username'], inst_name=request_dict['inst_name'])
    return redirect('users:profile', user_pk=user[0].pk)


def update_user_image(request):
    request_dict = request.POST
    user = CustomUser.objects.get(pk=request_dict['user'])
    image = request.FILES['image']
    user.image = image
    user.save()
    return redirect('users:profile', user_pk=user.pk)
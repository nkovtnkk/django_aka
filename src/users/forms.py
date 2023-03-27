from django.contrib.auth.forms import UserCreationForm
from .models import *


class RegisterForm(UserCreationForm):

   class Meta:
      model = CustomUser
      fields = ('username', 'password1', 'password2')


class ImageForm(UserCreationForm):

   class Meta:
      model = CustomUser
      fields = ['image']
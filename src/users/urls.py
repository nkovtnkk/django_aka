from django.urls import path

from .views import *


app_name = 'users'

urlpatterns = [
    path('<int:user_pk>', UserProfileView.as_view(), name='profile'),
    path('users_search', SearchUsersView.as_view(), name='users_search'),
    path('update_user_params', update_user_params, name='update_user_params'),
    path('update_user_image', update_user_image, name='update_user_image'),
    path('register', RegisterFormView.as_view(), name='register'),
    path('loging', login_user, name='login'),
    path('logout', logout_user, name='logout')
]
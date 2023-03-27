from django.urls import path

from .views import *


app_name = 'photos'

urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('crud_folder', CRUDFolder.as_view(), name='crud_folder'),
    path('create_post', create_post, name='create_post'),
    path('update_post', update_post, name='update_post'),
    path('delete_post', delete_post, name='delete_post')
]
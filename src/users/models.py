from django.db import models

from django.shortcuts import reverse

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    GENDERS = (
        ('m', 'Мужской'),
        ('f', 'Женский'),
        ('n', 'Не указан'),
    )

    image = models.ImageField(default='default_image/unknow.jpg', blank=True, verbose_name='Изображение профиля',
                              upload_to='profile_image/')
    sex = models.CharField('Пол', max_length=1, choices=GENDERS, default='')
    inst_name = models.CharField('Instagram', max_length=25, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'user_pk': self.pk})


class RandomUser(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_id')
    random_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='random_user_id')
    time_expired = models.DateTimeField(auto_now_add=True)

from django.db import models


class Folder(models.Model):

    name = models.CharField(max_length=100)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} - {self.name}'


class Post(models.Model):

    image = models.ImageField()
    text = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} - {self.text[:5]}'


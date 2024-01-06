from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Link(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    original_url = models.URLField(verbose_name='Исходная ссылка')
    short_code = models.CharField(max_length=15, unique=True, verbose_name='Короткая ссылка')
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.original_url} -> {self.short_code}'

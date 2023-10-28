from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    company_name = models.CharField(max_length=100, verbose_name='Имя компании')
    full_addres = models.CharField(max_length=100, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


    def __str__(self) -> str:
        return self.user.username
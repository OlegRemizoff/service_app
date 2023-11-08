from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client
from services.task import set_price


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя сервиса')
    full_price = models.PositiveIntegerField('Цена')

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self) -> str:
        return self.name

class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    )
    plan_types = models.CharField(choices=PLAN_TYPES, max_length=10, verbose_name='Тариф')
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self) -> str:
        return self.plan_types

class Subscripton(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT, verbose_name='Клиент')
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT, verbose_name='Сервис')
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT, verbose_name='Тарифный план')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')


    def save(self, *args, save_model=True, **kwargs):  # функция будет вызвана при создании или изменении модели
        if save_model:
            set_price.delay(self.id) # обновляем поле при помощи нашей функции и celery
        super().save(*args, **kwargs)   # обращаемся к базовому классу, чтобы вызвать метод save, а не перезаписать его


    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return 'Подписка'
    
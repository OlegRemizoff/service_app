from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client


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
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT, verbose_name='Подписка')
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT, verbose_name='Тарифный план')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return 'Подписка'
    
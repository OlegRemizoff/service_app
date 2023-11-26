from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client
from services.tasks import set_price, set_comment


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя сервиса')
    full_price = models.PositiveIntegerField('Цена')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price # фиксируем цену

    def save(self, *args, **kwargs):  # функция будет вызвана при создании или изменении модели
        if self.id: # 'Service' instance needs to have a primary key value before this relationship can be used.
            if self.full_price != self.__full_price: # если скидка изменилась, то изменим ее цену
                for subscription in self.subscriptions.all(): # related name из Subscription
                    set_price.delay(subscription.id) # обновляем поле при помощи нашей функции и celery
                    set_comment.delay(subscription.id)
            return super().save(*args, **kwargs)   # обращаемся к базовому классу, чтобы вызвать метод save, а не перез
        else:
            return super().save(*args, **kwargs)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent # фиксируем скидку

    def save(self, *args, **kwargs):  
        if self.id: # 'Service' instance needs to have a primary key value before this relationship can be used.
            if self.discount_percent != self.__discount_percent: 
                for subscription in self.subscriptions.all(): # related name из Subscription
                    set_price.delay(subscription.id) 
                    set_comment.delay(subscription.id)
            return super().save(*args, **kwargs) 
        else:
            return super().save(*args, **kwargs)

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
    comment = models.CharField(max_length=200, verbose_name="Комментарий", default='')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return 'Подписка {}'.format(self.id)
    

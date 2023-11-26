from celery import shared_task
from django.db.models import F
from django.db import transaction
from datetime import datetime
import time



@shared_task
def set_price(subscription_id):
    from .models import Subscripton

    with transaction.atomic(): # все применится либо не применится

        time.sleep(5)

        subscription = Subscripton.objects. filter(id=subscription_id).annotate(
            annotated_price=F("service__full_price") - 
                    F("service__full_price") * F("plan__discount_percent") / 100.00).first()
        
        time.sleep(20)

        subscription.price = subscription.annotated_price
        subscription.save()

@shared_task
def set_comment(subscription_id):
    from .models import Subscripton

    with transaction.atomic():

        time.sleep(5)

        subscription = Subscripton.objects.select_for_update().get(id=subscription_id)

        time.sleep(27)

        subscription.comment = str(datetime.now())
        subscription.save()
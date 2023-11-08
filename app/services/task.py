from celery import shared_task




@shared_task
def set_price(subscription_id):
    from .models import Subscripton
    
    subscription = Subscripton.objects.get(id=subscription_id)
    new_price = (subscription.service.full_price - 
                subscription.service.full_price * subscription.plan.discount_percent / 100 ) 
    subscription.service.full_price = new_price
    subscription.save(save_model=False)
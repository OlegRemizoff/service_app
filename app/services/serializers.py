from rest_framework import serializers
from .models import Subscripton, Plan





class PlanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Plan
        fields = '__all__'



class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField() # ищет функцию get_имя поля

    def get_price(self, instance): # instance = Subcriptions
        # return (instance.service.full_price - 
        #        (instance.service.full_price * instance.plan.discount_percent / 100))
        return instance.price # вычеслили в subsciprion.objects.all().annotate()

    class Meta:
        model = Subscripton
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')# plan_id-т.к ForeignKey, ссылается на Plan.id




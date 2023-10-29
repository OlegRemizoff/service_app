from rest_framework import serializers
from .models import Subscripton





class SubscriptionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')

    class Meta:
        model = Subscripton
        fields = ('id', 'plan_id', 'client_name', 'email') # plan_id - т.к ForeignKey, ссылается на Plan.id
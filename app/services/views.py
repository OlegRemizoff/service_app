from django.db.models import Prefetch, F
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscripton, Client
from .serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    # queryset = Subscripton.objects.all().prefetch_related('client').prefetch_related('client__user')
    queryset = Subscripton.objects.all().prefetch_related(
        'plan', # оптимизирует проблему n+1 - FROM "services_plan" WHERE "services_plan"."id" IN (2, 3)
        Prefetch('client', # присоединит клиентов where id in [1, 2....]
    queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')) # только нужные поля
    ).annotate(price=F("service__full_price") - 
                     F("service__full_price") * F("plan__discount_percent") / 100.00)
                     
    serializer_class = SubscriptionSerializer

''' n+1 при добавлении вложенного серализаторо plan
(0.000) SELECT "services_plan"."id", "services_plan"."plan_types", "services_plan"."discount_percent" FROM "services_plan" WHERE "services_plan"."id" = 3 LIMIT 21; args=(3,); alias=default
(0.000) SELECT "services_plan"."id", "services_plan"."plan_types", "services_plan"."discount_percent" FROM "services_plan" WHERE "services_plan"."id" = 2 LIMIT 21; args=(2,); alias=default
(0.000) SELECT "services_plan"."id", "services_plan"."plan_types", "services_plan"."discount_percent" FROM "services_plan" WHERE "services_plan"."id" = 3 LIMIT 21; args=(3,); alias=default
'''
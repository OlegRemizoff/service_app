from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscripton, Client
from .serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    # queryset = Subscripton.objects.all().prefetch_related('client').prefetch_related('client__user')
    queryset = Subscripton.objects.all().prefetch_related(
        Prefetch('client', # присоединит клиентов where id in [1, 2....]
    queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')) # только нужные поля
    )
    serializer_class = SubscriptionSerializer
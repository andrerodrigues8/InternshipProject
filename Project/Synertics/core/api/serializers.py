from rest_framework.serializers import ModelSerializer
from core.models import Trade

class TradeSerializer(ModelSerializer):
    class Meta:
        model=Trade
        fields='__all__'

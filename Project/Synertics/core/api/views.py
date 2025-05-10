from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import Trade
from core.views import calculations,variation_calc
from .serializers import TradeSerializer
@api_view(["GET"])
def getRoutes(request):
    routes=[
            "GET /api",
            "GET /api/chartdata",
            "GET /api/percentage",
            "GET /api/allprices",
            "GET /api/trades",
            ]
    return Response(routes)
@api_view(["GET"])
def getPricesfromchart(request):
    calc = calculations()
    response_data = {
        "dates": calc[0],
        "prices": calc[1],
    }
    return Response(response_data)
@api_view(["GET"])
def getPercentage(request):
    calc = calculations()
    variation=variation_calc(calc[1])
    response_data = {
        "variation": variation,
    }
    return Response(response_data)
@api_view(["GET"])
def getAllPrices(request):
    
    prices = list(Trade.objects.filter(
        instrument__icontains="BY"
    ).values_list("average_price_of_orders", flat=True))
    dates = list(Trade.objects.filter(
        instrument__icontains="BY"
    ).values_list("day", flat=True))
    dates = [str(date.strftime('%d/%m/%Y')) for date in dates]
    response_data = {
        "dates": dates,
        "prices": prices,
    }
    return Response(response_data)
@api_view(["GET"])
def getTrades(request):
    trades=Trade.objects.all()
    serializer=TradeSerializer(trades,many=True)
    return Response(serializer.data)

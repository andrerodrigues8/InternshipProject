from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Trade
import json
import logging
from decimal import Decimal
from .tasks import daily_scrape
logger = logging.getLogger(__name__)


def call_scraper(request):
    answer = daily_scrape()
    return JsonResponse({
        "message": "Scraping task initiated successfully",
        "result": answer
    })
def index(request):
    
  
    calc=calculations()
    variation=variation_calc(calc[1])
    context = {
        "dates": json.dumps(calc[0]),
        "prices": json.dumps(calc[1]),
        "variation": json.dumps(variation)
    }
    return render(request, "core/index.html", context)

def calculations():
    start_date = datetime.today() - timedelta(days=6)
    trades = {}
    
    for i in range(7):
        day = start_date + timedelta(days=i)
        if Trade.objects.filter(day=day.date()).exists():
            prices = list(Trade.objects.filter(
                day=day.date(),
                instrument__icontains="BY"
            ).values_list("average_price_of_orders", flat=True))
            if prices[0]!=0:
                trades[day.date()] = float(prices[0])
                logger.info(f"Found trades for {day.date()}: {trades[day.date()]}")
            else:
                logger.warning(f"No valid price data for {day.date()}")
        else:
            logger.warning(f"No trades found for {day.date()}")
    
    
    dates = [str(date.strftime('%d/%m/%Y')) for date in trades.keys()]
    prices = list(trades.values())
    
    
    return [dates,prices]
def variation_calc(prices):
    if len(prices) > 1:
        variation=round((prices[-1]-prices[-2])/prices[-2]*100,2)
    else:
        variation=0
    logger.info(f"Variation: {variation}")
    return variation

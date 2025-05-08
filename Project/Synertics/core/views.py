from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Trade
import json
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def home(request):
    return render(request, "core/home.html")

def index(request):
    logger.info("Entering index view")
    start_date = datetime.today() - timedelta(days=6)
    trades = {}
    
    for i in range(7):
        day = start_date + timedelta(days=i)
        logger.info(f"Checking trades for date: {day.date()}")
        if Trade.objects.filter(day=day.date()).exists():
            prices = list(Trade.objects.filter(
                day=day.date(),
                instrument__icontains="BY"
            ).values_list("average_price_of_orders", flat=True))
            # Only add to trades if we have valid price data
            if prices and prices[0] is not None:
                trades[day.date()] = float(prices[0])
                logger.info(f"Found trades for {day.date()}: {trades[day.date()]}")
            else:
                logger.info(f"No valid price data for {day.date()}")
        else:
            logger.info(f"No trades found for {day.date()}")
    
    # Convert dates to strings for JSON serialization
    dates = [str(date) for date in trades.keys()]
    prices = list(trades.values())
    
    logger.info(f"Final dates: {dates}")
    logger.info(f"Final prices: {prices}")
    
    context = {
        "dates": json.dumps(dates),
        "prices": json.dumps(prices)
    }
    
    return render(request, "core/index.html", context)




from django.urls import path
from . import views

urlpatterns=[
    path('',views.getRoutes),
    path('chartdata/',views.getPricesfromchart),
    path('percentage/',views.getPercentage),
    path('allprices/',views.getAllPrices),
    path('trades/',views.getTrades),
    path('trade/<str:pk>/',views.getTrade),
    path('trade/date/<str:date>/',views.getTradeByDate),
]

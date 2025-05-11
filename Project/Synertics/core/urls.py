from django.urls import path
from . import views

urlpatterns = [
       path("",views.index, name="index"),
       path("call_scraper",views.call_scraper, name="call_scraper"),
    
]
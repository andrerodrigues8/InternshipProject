from django.shortcuts import render
from django.http import JsonResponse
#from .tasks import periodic_task

# Create your views here.

world=2
def home(request):
    return render(request,"core/home.html")

def index(request):
    labels=["January","February","March","April","May","June","July"]
    data=[65,59,80,81,56,55,40]
    context={"labels":labels,"data":data}
    return render(request,"core/index.html",context)




from django.shortcuts import render
from django.http import HttpResponse
from .models import Chel

# Create your views here.
def index(request):
    return render(request, 'Glav.html',{'post':Chel.objects.values()})

def prof(request, Chel_id):
    return render(request,'Prof.html',{'Chel_id': Chel.objects.get(id_id=Chel_id)})
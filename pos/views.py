from django.shortcuts import render
from django.http import HttpResponse
from .models import Chel

# Create your views here.
def index(request):
    data=[]
    for i in Chel.objects.all():
        data.append((i.na,i.po))
    return render(request, 'Glav.html',{'post':Chel.objects.values()})
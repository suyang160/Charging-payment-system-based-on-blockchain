from django.shortcuts import render
from django.http import HttpResponse
from .models import ChargingPile
import json

# Create your views here.


def cp(request):
    return render(request, 'cp.html')

def order(request):
    return render(request, 'order.html')

def cpData(request):
    cp_list=[]

    for cp_info in ChargingPile.objects.all():
        cp_list.append({
            'DMID': cp_info.DMID,
            'name': cp_info.name,
            'installTime': cp_info.installTime,
            'brand': cp_info.brand,
            'category': cp_info.category,
            'gunNumber': cp_info.gunNumber,
            'ratedPower': cp_info.ratedPower,
            'version': cp_info.version,
            'state': cp_info.state,
            'chargingRecord': cp_info.chargingRecord,
            'location': cp_info.location,
        })
    result={"data":cp_list}
    return HttpResponse(json.dumps(result),content_type="application/json")
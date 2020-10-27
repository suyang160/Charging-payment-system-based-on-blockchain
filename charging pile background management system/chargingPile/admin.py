from django.contrib import admin

# Register your models here.
from .models import ChargingPile
from .models import Order

admin.site.register(ChargingPile)
admin.site.register(Order)
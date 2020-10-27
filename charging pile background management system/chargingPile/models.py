from django.db import models

# Create your models here.
class ChargingPile(models.Model):
    DMID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    installTime = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    gunNumber = models.CharField(max_length=200)
    ratedPower = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    chargingRecord = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    def __str__(self):
        return self.DMID

class Order(models.Model):
    orderContractAddress=models.CharField(max_length=200)
    chargingPileDMID = models.CharField(max_length=200)
    electricalVehicleDMID = models.CharField(max_length=200)
    createTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    orderState = models.CharField(max_length=200)
    chargingPower = models.CharField(max_length=200)
    tokenNeeded = models.CharField(max_length=200)
    tokenReceived = models.CharField(max_length=200)
    def __str__(self):
        return self.orderContractAddress
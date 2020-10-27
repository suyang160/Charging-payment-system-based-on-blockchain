from chargingPile.models import ChargingPile,Order
import sqlite3

if __name__ == "__main__":

    ChargingPile.objects.create(DMID="0x1234567890",name="上海",installTime="2020-1-1",brand="特来电",\
                                category="交流",gunNumber="1",ratedPower="7000W",version="V1.0",state="空闲",\
                                chargingRecord="查看",location="查看")
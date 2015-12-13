from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from decimal import *

class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=600)
    image_url = models.CharField(max_length=100)
    ask = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    closes = models.DateTimeField()

    def last_bid_at(self):
        bids = Bid.objects.filter(item=self).order_by('-created_at')
        if not bids:
            return self.created_at
        else:
            return bids[0].created_at

    def get_current_bid(self):
        bids = Bid.objects.filter(item=self).order_by('-price', 'created_at')
        if len(bids) == 0:
            return self.ask
        elif len(bids) == 1:
            return self.ask + Decimal(0.25)
        else:
            if bids[1].price == bids[0].price:
                return bids[1].price
            else:
                return bids[1].price + Decimal(0.25)

    def get_winner(self):
        bids = Bid.objects.filter(item=self).order_by('-price', 'created_at')
        if bids:
            return bids[0].user
        else:
            return None
    
    def get_time_left(self):
        now = datetime.now()
        naive = self.closes.replace(tzinfo=None)
        delta = naive - now
        ts = int(delta.total_seconds())
        if (ts<=0):
            return ""
        else:
            days = int(ts/86400)
            hours = int( (ts % 86400)/3600 )
            minutes = int( (ts % 3600)/60 )
            seconds = int( (ts % 60)/1 )
            arr = [days, hours, minutes, seconds]
            letters = "dhms"
            anything = False
            output = ""
            for i in xrange(4):
                if arr[i]: anything = True
                if anything:
                    output += (str(arr[i])+letters[i]+" ")
            return output[:-1]

class Bid(models.Model):
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

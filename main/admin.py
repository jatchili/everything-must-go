from django.contrib import admin

# Register your models here.
from .models import Item, Bid

admin.site.register(Item)
admin.site.register(Bid)
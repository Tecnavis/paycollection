from django.contrib import admin
from .models import CashCollection, Scheme,CashCollectionEntry

# Register your models here.
admin.site.register(CashCollection)
admin.site.register(Scheme)
admin.site.register(CashCollectionEntry)

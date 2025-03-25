from django.contrib import admin
from .models import Customer, Agent, CustomerAssignment

admin.site.register(Customer)
admin.site.register(Agent)
admin.site.register(CustomerAssignment)

# Register your models here.

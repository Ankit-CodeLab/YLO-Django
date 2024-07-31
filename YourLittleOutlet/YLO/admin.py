from django.contrib import admin
from YLO.models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Categorie)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
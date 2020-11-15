from django.contrib import admin
from main.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Media)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Resturant)
admin.site.register(ResturantAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
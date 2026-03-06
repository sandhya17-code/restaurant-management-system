from django.contrib import admin
from .models import Dish

class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')  
    # add fields you want to see as columns

admin.site.register(Dish, DishAdmin)
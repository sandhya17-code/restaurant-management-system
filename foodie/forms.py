from django import forms
from .models import Dish,Offer

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'image']
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['name','percentage','code','image']       
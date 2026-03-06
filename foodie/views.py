from django.shortcuts import render,redirect, get_object_or_404
from .models import Dish,Offer,Order,OrderItem
from .forms import DishForm,OfferForm
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.contrib.auth.models import User
import json
from django.contrib import messages
from django.http import JsonResponse

def home(request):
    return render(request,'home.html')

def admin_dashboard(request):
    if request.method == 'POST':
        # Create unbound forms first
        dish_form = DishForm()
        offer_form = OfferForm()

        # Check which form was submitted
        if 'submit_dish' in request.POST:
            dish_form = DishForm(request.POST, request.FILES)
            if dish_form.is_valid():
                dish_form.save()
                return redirect('admin_dashboard')

        elif 'submit_offer' in request.POST:
            offer_form = OfferForm(request.POST, request.FILES)
            if offer_form.is_valid():
                offer_form.save()
                return redirect('admin_dashboard')
    else:
        dish_form = DishForm()
        offer_form = OfferForm()

    dishes = Dish.objects.all()
    offers = Offer.objects.all()

    return render(request, 'admin_dashboard.html', {
        'dish_form': dish_form,
        'offer_form': offer_form,
        'dishes': dishes,
        'offers': offers,
    })
def menu(request):
    dishes = Dish.objects.all()
    return render(request, 'menu.html', {'dishes': dishes})

def offer(request):
    offers=Offer.objects.all()
    return render(request,'offer.html',{'offers':offers})

def edit_dish(request,id):
    dish = get_object_or_404(Dish,id=id)
    if request.method == "POST":
        form = DishForm(request.POST,instance=dish)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form=DishForm(instance=dish)
    return render(request,'edit_dish.html',{'form':form}) 
def delete_dish(request, id):
    dish = get_object_or_404(Dish, id=id)
    dish.delete()
    return redirect('admin_dashboard')

def edit_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
    if request.method == "POST":
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = OfferForm(instance=offer)
    return render(request, 'edit_offer.html', {'form': form})

def delete_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
    offer.delete()
    return redirect('admin_dashboard')

@login_required
def order(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    offers = list(Offer.objects.values("code","percentage"))
    offers_json = json.dumps(offers)

    # ✅ Get latest order for this user
    latest_order = Order.objects.filter(user=user).order_by('-id').first()
    latest_order_id = latest_order.id if latest_order else None

    return render(request, 'order.html', {
        "Receiver_name": user.first_name,
        "Receiver_address": profile.address,
        "offers_json": offers_json,
        "latest_order_id": latest_order_id   # ✅ Pass ID here too
    })


@login_required
def place_order(request):
    user = request.user
    order = Order.objects.create(user=user, status="Placed")

    dish_ids = request.POST.getlist("dish_ids")
    quantities = request.POST.getlist("quantities")

    for dish_id, qty in zip(dish_ids, quantities):
        try:
            dish = Dish.objects.get(id=dish_id)
            OrderItem.objects.create(
                order=order,
                dish=dish,
                quantity=int(qty),
                price=dish.price
            )
        except Dish.DoesNotExist:
            pass

    profile = Profile.objects.get(user=user)
    offers = list(Offer.objects.values("code","percentage"))
    offers_json = json.dumps(offers)

    return render(request, "order.html", {
        "latest_order_id": order.id,   # ✅ Pass order ID
        "Receiver_name": user.first_name,
        "Receiver_address": profile.address,
        "offers_json": offers_json
    })
@login_required
def cancel_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.can_cancel():   # ✅ enforce 10-min rule
            order.status = "Cancelled"
            order.save()
        return redirect("profile")  # redirect to orders list

@login_required
def profile_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile/order.html', {'orders': orders})

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

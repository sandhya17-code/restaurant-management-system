from django.urls import path
from .import views
urlpatterns=[
    path('',views.home,name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('menu.html/',views.menu,name='menu'),
    path('offer.html/',views.offer,name='offer'),
    path('dish/edit/<int:id>/',views.edit_dish,name='edit_dish'),
    path('dish/delete/<int:id>/',views.delete_dish,name='delete_dish'),
    path('offer/edit/<int:id>/',views.edit_offer,name='edit_offer'),
    path('offer/delete/<int:id>/',views.delete_offer,name='delete_offer'),
    path('order.html/',views.order,name='order'),
    path('place_order/',views.place_order,name="place_order"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('cancel_order/<int:order_id>/',views.cancel_order,name="cancel_order"),
    path('orders/', views.profile_orders,name='profile_orders'),
]

from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('profile/',views.profile_view,name="profile"),
]


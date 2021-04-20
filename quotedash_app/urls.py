from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('quotes', views.quotes),
    path('login', views.login),
    path('logout', views.logout),
    path('add_quote', views.add_quote),
    path('delete/<int:id_from_route>', views.delete_quote),
    path('like/<int:id_from_route>', views.like),
    path('unlike/<int:id_from_route>', views.unlike),
    path('user/<int:id_from_route>', views.user),
    path('myaccount/<int:id_from_route>', views.myaccount),
    path('myaccount/<int:id_from_route>/edit_user', views.edit_user),
]

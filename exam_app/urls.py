from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('wishes', views.dashboard),
    path('wish', views.wish),
    path('wish/new', views.new_wish),
    path('create_wish', views.create_wish),
    # path('grant/<int:wish_id>', views.granted_wish),
    path('wish/edit/<int:wish_id>', views.edit),
    path('wish/update/<int:wish_id>', views.update),
    path('delete_wish', views.delete),
]
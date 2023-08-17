from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('add_dish/', views.add_dish, name='add_dish'),
    path('remove_dish/<int:dish_id>/', views.remove_dish, name='remove_dish'),
    path('update_availability/<int:dish_id>/', views.update_availability, name='update_availability'),
    path('take_order/', views.take_order, name='take_order'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('review_orders/', views.review_orders, name='review_orders'),
    path('exit/', views.exit_system, name='exit_system'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
]
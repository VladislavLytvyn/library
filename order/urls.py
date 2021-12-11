from django.urls import path
from .views import get_all, OrderFormView
from order import views

urlpatterns = [
    path('', get_all, name='order'),
    path('form/', OrderFormView.as_view(), name='order_form'),
    path('<int:order_pk>/', views.view_order, name='view_order'),
    path('<int:order_pk>/delete/', views.delete_order, name='delete_order'),
]

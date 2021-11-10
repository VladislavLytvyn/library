from django.urls import path
from .views import get_all, OrderFormView

urlpatterns = [
    path('', get_all, name='order'),
    path('form/', OrderFormView.as_view(), name='order_form')
]

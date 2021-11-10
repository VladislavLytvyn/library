from django.urls import path
from .views import CustomUserFormView, loginuser


urlpatterns = [
    path('form/', CustomUserFormView.as_view(), name='customuser_form'),
    path('login/', loginuser, name='login'),
]

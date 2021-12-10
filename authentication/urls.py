from django.urls import path
from .views import (CustomUserFormView,
                    loginuser,
                    signupuser,
                    logoutuser)


urlpatterns = [
    path('form/', CustomUserFormView.as_view(), name='customuser_form'),
    path('login/', loginuser, name='loginuser'),
    path('logout/', logoutuser, name='logoutuser'),
    path('signup/', signupuser, name='signupuser'),
]

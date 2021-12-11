from django.urls import path
from .views import (loginuser,
                    signupuser,
                    logoutuser)


urlpatterns = [
    ## Creating a user on the site. Implementation of the form through the model on the fly.
    ## Add import CustomUserFormView.
    ## path('form/', CustomUserFormView.as_view(), name='customuser_form'),

    # path('login/', loginuser, name='loginuser'),
    # path('logout/', logoutuser, name='logoutuser'),
    # path('signup/', signupuser, name='signupuser'),
]

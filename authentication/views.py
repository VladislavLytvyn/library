from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormFromModelCustomUser, UserCreationFormWithEmail
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import CustomUser


def signupuser(request):
    if request.method == "GET":
        return render(request, 'authentication/signupuser.html', {'form': UserCreationFormWithEmail()})
    else:
        # это очень смешно что в форме написаны кучу правил валидации пароля при реге а я сделал чувака с паролем 1))
        if request.POST['password1'] == request.POST['password2']:
            try:
                # when standard AUTH_USER_MODEL:
                # user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                # when CustomUser AUTH_USER_MODEL:
                user = CustomUser.objects.create_user(email=request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return render(request, 'authentication/succesfullogin.html')
            except IntegrityError:
                return render(request, 'authentication/signupuser.html', {'form': UserCreationFormWithEmail(),
                                                                          'error': "Please choose another email"})
        else:
            return render(request, 'authentication/signupuser.html', {'form': UserCreationFormWithEmail(),
                                                                      'error': 'Password did not math'})


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return render(request, 'homepage/homepage.html')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'authentication/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'authentication/loginuser.html', {'form': AuthenticationForm(), 'error': 'No username or password found'})
        else:
            login(request, user)
            return render(request, 'authentication/succesfullogin.html')


# Creating a user on the site. Implementation of the form through the model on the fly.
# The user does not enter the site.
# class CustomUserFormView(FormView):
#     form_class = FormFromModelCustomUser
#     template_name = 'authentication/customuser_form.html'
#     success_url = reverse_lazy('customuser_form')
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

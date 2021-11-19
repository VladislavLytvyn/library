from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import FormFromModelCustomUser
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import CustomUser


class CustomUserFormView(FormView):
    form_class = FormFromModelCustomUser
    template_name = 'authentication/customuser_form.html'
    success_url = reverse_lazy('customuser_form')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def signupuser(request):
    if request.method == "GET":
        return render(request, 'authentication/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # when standard AUTH_USER_MODEL:
                # user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user = CustomUser.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return render(request, 'authentication/succesfullogin.html')
            except IntegrityError:
                return render(request, 'authentication/signupuser.html', {'form': UserCreationForm(),
                                                                          'error': "Please choose another username"})
        else:
            return render(request, 'authentication/signupuser.html', {'form': UserCreationForm(),
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
            return render(request, 'authentication/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not math'})
        else:
            login(request, user)
            # return redirect('succesfullogin')
            return render(request, 'authentication/succesfullogin.html')

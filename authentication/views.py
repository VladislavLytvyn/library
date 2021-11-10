from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormFromModelCustomUser
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login


class CustomUserFormView(FormView):
    form_class = FormFromModelCustomUser
    template_name = 'authentication/customuser_form.html'
    success_url = reverse_lazy('customuser_form')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'authentication/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'authentication/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not math'})
        else:
            login(request, user)
            # return redirect('succesfullogin')
            return render(request, 'authentication/succesfullogin.html')  #  перевод на дом сторінку??

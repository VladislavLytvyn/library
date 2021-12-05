from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class FormFromModelCustomUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'email', 'password', 'role', 'is_active']


class UserCreationFormWithEmail(UserCreationForm):
    UserCreationForm.Meta.fields = ('email',)

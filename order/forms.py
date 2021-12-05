from django import forms
from .models import Order


FILTERING_CHOICES = (
    ("show all", "Show all orders"),
    # ("show specific user books", "Show all books ordered by specific user (enter user id)"),
    ("all sort be create date", "Show all orders sorted by created date"),
    ("all sort by planed date", "Show all orders sorted by planed date"),
    ("not return in time", "Show all users who does not hand over books on time"),
)


class OrderFiltersForm(forms.Form):
    filter_methods = forms.ChoiceField(choices=FILTERING_CHOICES,
                                       widget=forms.Select(attrs={'id': "inputState",
                                                                  'class': "form-control"}))
    search_param = forms.CharField(required=None,
                                   widget=forms.TextInput(attrs={'class': "form-control mr-sm-2",
                                                                 'placeholder': "Input text"}))


class FormFromModelOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

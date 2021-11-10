from django import forms
from .models import Author


FILTERING_CHOICES = (
    ("show all", "Show all authors with their books"),
    ("show specific author", "Show specific author with his books (enter id)"),
)


class AuthorFiltersForm(forms.Form):
    filter_methods = forms.ChoiceField(choices=FILTERING_CHOICES,
                                       widget=forms.Select(attrs={'id': "inputState",
                                                                  'class': "form-control"}))
    search_param = forms.CharField(required=None,
                                   widget=forms.TextInput(attrs={'class': "form-control mr-sm-2",
                                                                 'placeholder': "Input text"}))


class FormFromModelAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"

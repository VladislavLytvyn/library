from django import forms
from .models import Author

# почитай, подумай, поймешь что этот селект не нужен в принципе
CHOICE = (
    # это не нужно. если селект пустой значит показывай всех авторов по умолчанию
    ("show all", "Show all authors with their books"),
    # мы ищем автора по имени-фамилии но точно не по айди. айди это внутреняя штука, никто не должен знать какой там у кого айди
    # это не секрет, не нужно заморачиваться чтобы никто не знал айдишку. но и искать по ней точно не стоит
    ("show specific author", "Show specific author with his books (enter id)"),
)


# так гораздо читаемее, правда?)
class AuthorFiltersForm(forms.Form):
    filter_methods = forms.ChoiceField(
        choices=CHOICE,
        widget=forms.Select(
            attrs={
                'id': "inputState",
                'class': "form-control"
            }
        )
    )
    search_param = forms.CharField(
        required=None,
        widget=forms.TextInput(
            attrs={
                'class': "form-control mr-sm-2",
                'placeholder': "Input text"
            })
    )


class FormFromModelAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "surname", "patronymic"]

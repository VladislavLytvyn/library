from django import forms
from .models import Book


CHOICE = (
    ("all", "Show all books"),
    ("book_id", "Show specific book (enter id)"),
    ("book_name", "Show specific book (enter name of book)"),
    ("unordered", "Show all unordered book"),
    ("author_name", "Show all books by name of author"),
    ("all_name_sorted_asc", "Show all books sorted by name asc"),
    ("all_name_sorted_desc", "Show all books sorted by name desc"),
    ("all_count_sorted_asc", "Show all books sorted by count (ascending)"),
    ("all_count_sorted_desc", "Show all books sorted by count (descending)"),
)


class BookForm(forms.Form):
    opt = forms.ChoiceField(choices=CHOICE,
                            label="",
                            widget=forms.Select(attrs={'id': "inputState",
                                                       'class': "form-control"}))
    title = forms.CharField(label="",
                            required=False,
                            widget=forms.TextInput(attrs={'type': "search",
                                                          'class': "form-control mr-sm-2",
                                                          'aria-label': "Search"}))

    # title = forms.IntegerField(label="",
    #                            required=False,
    #                            widget=forms.NumberInput(attrs={'class': "form-control mr-sm-2",
    #                                                            'type': "search",
    #                                                            'aria-label': "Search"}))
                            # widget=forms.TextInput(attrs={'class': "form-control mr-sm-2",
                            #                               'type': "search",
                            #                               'aria-label': "Search"}))


class FormFromModelBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'count', 'description', 'authors']
        labels = {'authors': 'Author (press ctrl to select multiple authors)'}
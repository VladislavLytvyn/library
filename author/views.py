from django.shortcuts import render
from order.models import Order
from .models import Author
from .forms import AuthorFiltersForm, FormFromModelAuthor
from authentication.models import CustomUser
from book.models import Book
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy


get_all_books = Book.get_all()
get_all_authors = Author.get_all()


@csrf_protect
def get_all(request):
    context = {}
    context['form'] = AuthorFiltersForm()
    context['books'] = get_all_books
    if request.method == 'GET':
        context['authors'] = get_all_authors
    elif request.method == 'POST':
        form = AuthorFiltersForm(request.POST)
        get_select_value = form['filter_methods'].value()
        search_param = int(form['search_param'].value()) if form['search_param'].value() and form.is_valid() else None
        if get_select_value == "show specific author":
            context['authors'] = [Author.get_by_id(search_param)]
        else:
            context['authors'] = get_all_authors
    return render(request, 'author/author.html', context)


class AuthorFormView(FormView):
    form_class = FormFromModelAuthor
    template_name = "author/author_form.html"
    success_url = reverse_lazy("author_form")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

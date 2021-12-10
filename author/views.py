from django.shortcuts import render, get_object_or_404, redirect
from order.models import Order
from .models import Author
from .forms import AuthorFiltersForm, FormFromModelAuthor
from authentication.models import CustomUser
from book.models import Book
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy


@csrf_protect
def get_all(request):
    context = dict()
    context['form'] = AuthorFiltersForm()
    context['books'] = Book.get_all()
    if request.method == 'GET':
        context['authors'] = Author.get_all()
    elif request.method == 'POST':
        get_select_value = request.POST.get('filter_methods')
        get_input_value = request.POST.get('search_param')
        if get_select_value == "show specific author":
            try:
                context['authors'] = [Author.get_by_id(get_input_value)]
                if context['authors'] == [None]:
                    del context['authors']
                    context['error_author_id'] = 'Author does not exist'
                    return render(request, 'author/author.html', context)
            except ValueError:
                context['error_author_id'] = 'Author does not exist'
                return render(request, 'author/author.html', context)
        else:
            context['authors'] = Author.get_all()
    return render(request, 'author/author.html', context)


class AuthorFormView(FormView):
    form_class = FormFromModelAuthor
    template_name = "author/author_form.html"
    success_url = reverse_lazy("author_form")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def view_author(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    if request.method == 'GET':
        form_author = FormFromModelAuthor(instance=author)
        return render(request, 'author/change_author.html', {'author': author, 'form_author': form_author})
    else:
        try:
            form_author = FormFromModelAuthor(request.POST, instance=author)
            form_author.save()
            return redirect('author')
        except ValueError:
            return render(request, 'author/change_author.html', {'author': author,
                                                                 'form_author': form_author,
                                                                 'error': 'Bad information'})


def delete_author(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    if request.method == 'POST':
        author.delete()
        return redirect('author')


# author.delete() можна author.delete_by_id
# def delete_author(request, author_pk):
#     author = Author.get_by_id(author_pk)
#     if request.method == 'POST':
#         author.delete_by_id(author_pk)
#         # return redirect('author')
#         return redirect('author')

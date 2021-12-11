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
    # добавь дефолтный ордер бай по created_at
    # и почему это незалогиненый чел может менять записи в БД?
    context = dict()
    context['form'] = AuthorFiltersForm()
    context['books'] = Book.get_all()
    if request.method == 'GET':
        context['authors'] = Author.get_all()
    #серч это не пост а гет. проверяй гет параметры, если он есть - фильтруй. нет - не фильтруй. все
    elif request.method == 'POST':
        # постфикс _value не несет в себе никакого смысла
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

# вынеси в отдельный файл. это файль вьюс, тут должны быть вьюс
# я посмотрел - у тебя же есть файл формс. почему туда не вынес?
class AuthorFormView(FormView):
    form_class = FormFromModelAuthor
    template_name = "author/author_form.html"
    success_url = reverse_lazy("author_form")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def view_author(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    # это два разных метода. поставь нужный урл в <form action="....
    if request.method == 'GET':
        form_author = FormFromModelAuthor(instance=author)
        return render(request, 'author/change_author.html', {'author': author, 'form_author': form_author})
    else:
        try:
            # я только что сделал автора с пустыми полями. нет валидации вообще. я думаю она должна быть в форме
            form_author = FormFromModelAuthor(request.POST, instance=author)
            form_author.save()
            # редиректи на список авторов. потому что человек не поймет что автор добавлен и нажмет еще 5 раз и сделает 5 одинаковых авторов
            return redirect('author')
        except ValueError:
            return render(request, 'author/change_author.html', {'author': author,
                                                                 'form_author': form_author,
                                                                 'error': 'Bad information'})


def delete_author(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    # я не понимаю, в url.py нельзя что ли поставить метод к урлу? что это за бесконечные проверки метода?
    # и вообще если это не пост зачем запускать строку выше?
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

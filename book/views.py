from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from author.models import Author
from authentication.models import CustomUser
from order.models import Order
from django.views.generic import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from .forms import BookForm, FormFromModelBook
from django.urls import reverse_lazy, NoReverseMatch


@csrf_protect
def get_all(request):

    form = BookForm()
    books = None

    if request.method == 'GET':
        books = Book.get_all()

    elif request.method == 'POST':
        get_select_value = request.POST.get('opt')
        get_input_value = request.POST.get('title')
        if get_select_value == 'book_id':
            try:
                books = [Book.get_by_id(int(get_input_value))]
                if books == [None]:
                    return render(request, 'book/book.html', {'form': form,
                                                              'error_book_id': 'Book does not exist'})
            except (ValueError, NameError):
                return render(request, 'book/book.html', {'books': books,
                                                          'form': form,
                                                          'error_book_id': 'Book does not exist'})
        elif get_select_value == 'book_name':
            books = show_books_by_name_book(get_input_value)
            if not books:
                return render(request, 'book/book.html', {'form': form,
                                                          'error_book_id': 'Book does not exist'})
        elif get_select_value == 'author_name':
            books = show_books_by_name_author(get_input_value)
            if not books:
                return render(request, 'book/book.html', {'form': form,
                                                          'error_book_id': 'Book does not exist'})
        elif get_select_value == 'all_name_sorted_asc':
            books = Book.objects.all().order_by('name')
        elif get_select_value == 'all_name_sorted_desc':
            books = Book.objects.all().order_by('-name')
        elif get_select_value == 'all_count_sorted_asc':
            books = Book.objects.all().order_by('count')
        elif get_select_value == 'all_count_sorted_desc':
            books = Book.objects.all().order_by('-count')
        elif get_select_value == 'unordered':
            books = get_unordered_books()
        else:
            books = Book.get_all()

    return render(request, 'book/book.html', {'books': books,
                                              'form': form})


def show_books_by_name_book(get_input_value):
    result_name = []
    for book in Book.get_all():
        if book.name == get_input_value:
            result_name.append(book)
    return result_name


def show_books_by_name_author(get_input_value):
    res = []
    for elem in Book.get_all():
        for br in elem.authors.all():
            if br.name == get_input_value or br.surname == get_input_value or br.patronymic == get_input_value:
                res.append(elem)
    return res


def get_unordered_books():
    all_books = Book.get_all()
    all_orders = Order.get_all()
    get_all_ordered_books = []
    for book in all_books:
        for order in all_orders:
            if book.id == order.book.id:
                get_all_ordered_books.append(book)
    get_all_unordered_books = set(all_books) - set(get_all_ordered_books)
    return get_all_unordered_books


class BookFormView(FormView):
    form_class = FormFromModelBook
    template_name = "book/book_form.html"
    success_url = reverse_lazy("book_form")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def view_book(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'GET':
        form_book = FormFromModelBook(instance=book)
        return render(request, 'book/change_book.html', {'book': book, 'form_book': form_book})
    else:
        try:
            form_book = FormFromModelBook(request.POST, instance=book)
            form_book.save()
            return redirect('book')
        except ValueError:
            return render(request, 'book/change_book.html', {'book': book,
                                                             'form_book': form_book,
                                                             'error': 'Bad information'})


def delete_book(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book')

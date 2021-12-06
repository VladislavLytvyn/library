from django.urls import path
from django.conf.urls import url
from .views import get_all, BookFormView
from book import views


urlpatterns = [
    path('', get_all, name='book'),
    path('form/', BookFormView.as_view(), name='book_form'),
    path('<int:book_pk>/', views.view_book, name='view_book'),
    path('<int:book_pk>/delete/', views.delete_book, name='delete_book'),
    # path('<int:book_pk>/get_book', get_all),
    url(r'^page/(\d+)/$', get_all),
]

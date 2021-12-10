from django.urls import path
from .views import get_all
from .views import BookFormView


urlpatterns = [
    path('', get_all, name='book'),
    path('form/', BookFormView.as_view(), name='book_form')
]

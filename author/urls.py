from django.urls import path
from .views import get_all, AuthorFormView


urlpatterns = [
    path('', get_all, name='author'),
    path('form/', AuthorFormView.as_view(), name='author_form')
]

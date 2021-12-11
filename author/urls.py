from django.urls import path
from .views import get_all, AuthorFormView
from author import views


urlpatterns = [
    path('', get_all, name='author'),
    path('form/', AuthorFormView.as_view(), name='author_form'),
# ахах, а почему author_pk а не author_id? это прикол джанги?
    path('<int:author_pk>/', views.view_author, name='view_author'),
    path('<int:author_pk>/delete/', views.delete_author, name='delete_author'),
]

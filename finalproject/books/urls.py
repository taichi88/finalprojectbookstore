
from django.urls import path
from . import views

urlpatterns = [
    path("mylist/", views.BookCollectionView.as_view(), name='book_collection'),  # Collection of books
    path("<int:pk>/", views.BookSingletonView.as_view(), name='book_singleton'),  # Individual book by primary key
    path('list/', views.BookListView.as_view(), name='book_list'),  # List of all books

]

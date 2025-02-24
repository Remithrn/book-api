from django.urls import path
from .views import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    ReadingListListCreateAPIView,
    ReadingListRetrieveUpdateDestroyAPIView,
    AddBookToReadingListAPIView,
    RemoveBookFromReadingListAPIView,
    UpdateReadingListItemOrderAPIView,
)

urlpatterns = [
    path("books/", BookListCreateAPIView.as_view(), name="book-list-create"),
    path(
        "books/<int:pk>/",
        BookRetrieveUpdateDestroyAPIView.as_view(),
        name="book-detail",
    ),
    path(
        "readinglists/",
        ReadingListListCreateAPIView.as_view(),
        name="readinglist-list-create",
    ),
    path(
        "readinglists/<int:id>/",
        ReadingListRetrieveUpdateDestroyAPIView.as_view(),
        name="readinglist-detail",
    ),
    path(
        "readinglists/<int:reading_list_id>/add_book/",
        AddBookToReadingListAPIView.as_view(),
        name="readinglist-add-book",
    ),
    path(
        "readinglists/<int:reading_list_id>/remove_book/<int:item_id>/",
        RemoveBookFromReadingListAPIView.as_view(),
        name="readinglist-remove-book",
    ),
    path(
        "readinglists/<int:reading_list_id>/update_item/<int:pk>/",
        UpdateReadingListItemOrderAPIView.as_view(),
        name="update-reading-list-item-order",
    ),
]

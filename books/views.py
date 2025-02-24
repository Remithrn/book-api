from rest_framework import generics, status
from .models import Book, ReadingListBook, ReadingList
from rest_framework.response import Response
from .serializers import (
    BookSerializer,
    ReadingListItemSerializer,
    ReadingListSerializer,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import models


class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all books.
    POST: Create a new book (authentication required).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific book.
    PUT/PATCH: Update a book (authentication required).
    DELETE: Remove a book (authentication required).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ReadingListListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all reading lists for the authenticated user.
    POST: Create a new reading list.
    """

    serializer_class = ReadingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReadingListRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific reading list.
    PUT/PATCH: Update the reading list.
    DELETE: Delete the reading list.
    """

    serializer_class = ReadingListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)


class AddBookToReadingListAPIView(generics.CreateAPIView):
    """
    POST: Add a book to a reading list.
    """

    serializer_class = ReadingListItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, reading_list_id):
        reading_list = get_object_or_404(
            ReadingList, id=reading_list_id, user=request.user
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data["book"]

        # Check if the book is already in the reading list.
        if reading_list.items.filter(book=book).exists():
            return Response(
                {"detail": "This book is already in the reading list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        last_order = (
            reading_list.items.aggregate(max_order=models.Max("order"))["max_order"]
            or 0
        )
        serializer.save(reading_list=reading_list, order=last_order + 1)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveBookFromReadingListAPIView(generics.DestroyAPIView):
    """
    DELETE: Remove a book (item) from a reading list.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, reading_list_id, item_id):
        reading_list = get_object_or_404(
            ReadingList, id=reading_list_id, user=request.user
        )
        item = get_object_or_404(ReadingListBook, id=item_id, reading_list=reading_list)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateReadingListItemOrderAPIView(generics.UpdateAPIView):
    """
    PATCH: Update the order of a reading list item.
    """

    serializer_class = ReadingListItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure the item belongs to a reading list owned by the current user.
        return ReadingListBook.objects.filter(reading_list__user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        new_order = request.data.get("order")
        if new_order is None:
            return Response(
                {"error": "Order not provided."}, status=status.HTTP_400_BAD_REQUEST
            )
        instance.order = new_order
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

from rest_framework import serializers
from .models import Book, ReadingList, ReadingListBook


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ReadingListItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source="book", write_only=True
    )

    class Meta:
        model = ReadingListBook
        fields = ("id", "book", "book_id", "order")


class ReadingListSerializer(serializers.ModelSerializer):
    items = ReadingListItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingList
        fields = ("id", "name", "items")

# api/models.py
from django.db import models
from django.conf import settings


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)  # Comma-separated list of authors
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class ReadingList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reading_lists", on_delete=models.CASCADE
    )
    books = models.ManyToManyField(
        Book, through="ReadingListBook", related_name="reading_lists"
    )

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class ReadingListBook(models.Model):
    reading_list = models.ForeignKey(
        ReadingList, related_name="items", on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("reading_list", "book")
        ordering = ["order"]

    def __str__(self):
        return f"{self.book.title} in {self.reading_list.name}"

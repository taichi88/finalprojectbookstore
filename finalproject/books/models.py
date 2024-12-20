
from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    borrower = models.ForeignKey(
        User,
        related_name="borrowed_books",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )  # Borrower of the book
    user = models.ForeignKey(User, related_name="books",on_delete=models.CASCADE)



    def __str__(self):
        return self.title


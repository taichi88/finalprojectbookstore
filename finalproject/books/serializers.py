from rest_framework import serializers
from .models import Book





class BookSerializer(serializers.ModelSerializer):
    owner_is = serializers.CharField(source="user.username", read_only=True)  # Custom field for user's name
    Borrower_is = serializers.CharField(source="borrower.username", read_only=True)  # Borrower's name

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'owner_is', 'Borrower_is']
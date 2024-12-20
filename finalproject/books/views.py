from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookCollectionView(APIView):
    """Handles collection of books for the authenticated user."""
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    @swagger_auto_schema(
        responses={200: BookSerializer(many=True)},
        operation_summary="Get all books for the authenticated user."
    )
    def get(self, request):
        books = request.user.books.all()  # Get books related to the authenticated user
        serializer = self.serializer_class(instance=books, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=BookSerializer,
        responses={201: BookSerializer()},
        operation_summary="Create a new book for the authenticated user."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)  # Associate the book with the authenticated user
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class BookSingletonView(APIView):
    """Handles individual book operations."""
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    @swagger_auto_schema(
        responses={200: BookSerializer()},
        operation_summary="Retrieve a single book by its ID."
    )
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = self.serializer_class(instance=book)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=BookSerializer,
        responses={202: BookSerializer()},
        operation_summary="Update specific fields of a book by its ID."
    )
    def patch(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = self.serializer_class(data=request.data, instance=book, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(
        responses={204: "No Content"},
        operation_summary="Delete a book by its ID."
    )
    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookListView(generics.ListAPIView):
    """Lists all books in the system."""
    queryset = Book.objects.all()  # Get all books
    serializer_class = BookSerializer
      # Ensure the user is authenticated to view the list

    @swagger_auto_schema(
        operation_summary="Get a list of all books in the system.",
        responses={200: BookSerializer(many=True)}
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class BorrowBookView(APIView):
    """Allows a user to borrow a book."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: BookSerializer()},
        operation_summary="Borrow a book.",
        operation_description="Set the borrower of the book to the authenticated user.")

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        # Check if the book already has a borrower
        if book.borrower:
            return Response({"error": "This book is already borrowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the borrower as the authenticated user
        book.borrower = request.user
        book.save()

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

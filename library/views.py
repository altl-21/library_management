from django.shortcuts import render
from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.conf import settings

from .models import Book, Loan
from .utils import send_email
from .serializers import UserSerializer, BookSerializer, LoanSerializer

# Create your views here.
class UserRegistration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User created successfully'}, status=201)

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'availability']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'author']


    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to add a book.")

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this book.")

    def perform_destroy(self, instance):
        if self.request.user.is_superuser:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this book.")

class LoanBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if book.availability:
            Loan.objects.create(user=request.user, book=book)
            book.availability = False
            book.save()

            html_content = f'You have borrowed the book: {book.title}'
            send_email('Book borrowed successfully', html_content, settings.RECEPTION_EMAIL)

            return Response({'message': 'Book borrowed successfully'}, status=200)
        else:
            return Response({'error': 'Book is not available'}, status=400)

class ReturnBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        loan = get_object_or_404(Loan, book_id=pk, user=request.user, returned_at__isnull=True)
        loan.returned_at = timezone.now()
        loan.save()
        loan.book.availability = True
        loan.book.save()

        html_content = f'You have returned the book: {loan.book.title}'
        send_email('Book Returned', html_content, settings.RECEPTION_EMAIL)

        return Response({'message': 'Book returned successfully'}, status=200)
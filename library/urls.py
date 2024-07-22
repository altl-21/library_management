from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserRegistration, BookListView, BookDetailView, LoanBookView, ReturnBookView

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/borrow/', LoanBookView.as_view(), name='borrow-book'),
    path('books/<int:pk>/return/', ReturnBookView.as_view(), name='return-book'),
]
# Library Management System

## Overview

This project is a Library Management System built with Django and Django REST Framework. It allows users to search for books, borrow them, and manage their accounts. Library administrators can add new books, manage users, and track borrowed books.

## Features

- User registration and login
- JWT authentication
- Browse, search, and view detailed book information
- Borrow and return books with email notifications
- Admin functionalities to add/remove books and manage users
- Filtering and pagination for books
- Full-text search by title and author
- Secure against CSRF, XSS, and SQL Injection attacks

## Prerequisites

- Python 3.10 or later(I used 3.11.0)
- Django(I used 5.06)
- Django REST Framework
- PostgreSQL
- Docker (for containerized setup)
- Git (for version control)
- Heroku CLI (for deployment)

## Installation

### Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Database

Update the DATABASES setting in library_management/settings.py to point to your PostgreSQL database.

### Terminal for running server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Example API Requests

- #### Register a New User
```bash
curl -X GET "http://127.0.0.1:8000/api/register/"

payload = {
    "username": "newuser",
    "password": "password123",
    "email": "newuser@example.com"
}
```

- #### Obtain JWT Token
```bash
curl -X GET "http://127.0.0.1:8000/api/login/"

payload = {
    "username": "newuser",
    "password": "password123"
}

response = {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJ..."
}
```

- #### Get List of Books
```bash
curl -X GET "http://127.0.0.1:8000/api/books/"
```
- #### Filter Books by Author
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?author=John%20Doe"
```
- #### Search Books by Title
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?search=Python"
```
- #### Paginate Books
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?page=2"
```

### API Documentation

The API documentation is automatically generated using Swagger and is available at /swagger/.